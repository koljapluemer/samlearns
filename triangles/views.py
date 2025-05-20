from django.shortcuts import render, redirect
from django.contrib import messages
from guest_user.decorators import allow_guest_user
import string
import re

from triangles.models import ClozeTemplate
from triangles.utils import get_due_topic, get_due_gap_index_for_cloze_template, get_random_relevant_distractor

def clean_word(word):
    """Remove non-alphanumeric characters from the beginning and end of the word."""
    # Remove punctuation and whitespace from both ends
    cleaned = word.strip(string.punctuation + string.whitespace)
    return cleaned

@allow_guest_user
def render_cloze_exercise(request, template_id, gap_index, level):
    template = ClozeTemplate.objects.get(id=template_id)
    gap_index = int(gap_index)
    level = int(level)
    
    # Split content into words
    words = template.content.split()
    
    # Get the word at the gap index and clean it
    correct_word = clean_word(words[gap_index])
    
    # Get a relevant distractor
    distractor = get_random_relevant_distractor(correct_word)
    
    # Create cloze text by replacing the word with a gap
    # Keep any punctuation that was part of the original word
    original_word = words[gap_index]
    punctuation_before = re.match(r'^[^\w]*', original_word).group()
    punctuation_after = re.search(r'[^\w]*$', original_word).group()
    words[gap_index] = f"{punctuation_before}_____{punctuation_after}"
    cloze_text = " ".join(words)
    
    if request.method == 'POST':
        user_answer = clean_word(request.POST.get('answer', ''))
        if user_answer == correct_word:
            messages.success(request, "Correct!")
        else:
            messages.error(request, f"Wrong! The correct answer was: {correct_word}")
    
    # Prepare answer options
    answer_options = [correct_word, distractor.content] if distractor else [correct_word]
    
    context = {
        'cloze_text': cloze_text,
        'template_id': template_id,
        'gap_index': gap_index,
        'level': level,
        'answer_options': answer_options,
    }
    return render(request, 'triangles/cloze.html', context)

@allow_guest_user
def redirect_to_next_exercise(request):
    topic = get_due_topic()
    if not topic:
        messages.error(request, "No topics available")
        return redirect('triangles:index')
        
    template = topic.cloze_templates.first()
    if not template:
        messages.error(request, "No exercises available for this topic")
        return redirect('triangles:index')
        
    gap_index = get_due_gap_index_for_cloze_template(request.user, template)
    return redirect('triangles:cloze', 
                   template_id=template.id,
                   gap_index=gap_index,
                   level=1)