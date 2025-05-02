from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.conf import settings

from openai import OpenAI
from pydantic import BaseModel
from german_with_videos.models import Video, VideoStatus, Word, Meaning, Snippet

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class WordEntry(BaseModel):
    word: str
    meaning: str

class WordEntryResponse(BaseModel):
    words: list[WordEntry]

def get_words_with_translations(text: str) -> list:
    """Get words and translations for a given text"""
    prompt = (
        "You are an expert in German. "
        "Extract language learning vocabulary from the following text, ignoring proper nouns like restaurant names, "
        "exclamations such as 'oh', and other non-translatable words. For each extracted word, provide an English translation suitable to learn the word on its own."
        "Retain correct capitalization and spelling. If a word appears in a declined, conjugated, or plural form, "
        "add both the occurring and base form as separate entries (e.g. for 'Bäume' and 'Baum', or 'Sie lief' and 'laufen'), both including the translation. Return your answer as a structured list of vocab."
    )
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt + f"\n\nText: {text}\n\nOutput JSON:"}
            ],
            response_format=WordEntryResponse,
        )
        return response.choices[0].message.parsed.words
    except Exception as e:
        print(f"Error processing text snippet: {e}")
        return []



@staff_member_required
@require_http_methods(["POST"])
def generate_translations(request, youtube_id):
    """View to generate translations for all snippets in a video"""
    try:
        video = Video.objects.get(youtube_id=youtube_id)
        
        if not video.snippets.exists():
            messages.error(request, "No snippets available. Please generate snippets first.")
            return redirect('cms:german_with_videos:video_details', youtube_id=youtube_id)
        
        # Delete existing words and meanings
        Word.objects.filter(videos=video).delete()
        
        # Process each snippet
        for snippet in video.snippets.all():
            # Get words and translations for this snippet
            words_with_translations = get_words_with_translations(snippet.content)
            
            # Process each word
            for word_entry in words_with_translations:
                # Get or create the word
                word_obj, _ = Word.objects.get_or_create(
                    original_word=word_entry.word
                )
                
                # Add the video and snippet to the word's relationships
                word_obj.videos.add(video)
                word_obj.occurs_in_snippets.add(snippet)
                
                # Create the meaning
                Meaning.objects.create(
                    word=word_obj,
                    en=word_entry.meaning,
                    snippet_context=snippet,
                    creation_method="ChatGPT 1.0.0"
                )
        
        # Update video status
        video.status = VideoStatus.SNIPPETS_AND_TRANSLATIONS_GENERATED
        video.save()
        
        messages.success(request, "Successfully generated translations for all snippets.")
            
    except Video.DoesNotExist:
        messages.error(request, "Video not found.")
    except Exception as e:
        messages.error(request, f"Error generating translations: {str(e)}")
    
    return redirect('cms:german_with_videos:video_details', youtube_id=youtube_id)

