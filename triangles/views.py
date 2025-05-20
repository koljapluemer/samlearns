from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from guest_user.decorators import allow_guest_user
import string
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from triangles.models import ClozeTemplate, Topic, TopicProgress, ClozeTemplateGapProgress, LearningEvent, Distractor
from triangles.utils import get_due_topic, get_due_gap_index_for_cloze_template, get_random_relevant_distractor

def clean_word(word):
    """Remove non-alphanumeric characters from the beginning and end of the word."""
    # Remove punctuation and whitespace from both ends
    cleaned = word.strip(string.punctuation + string.whitespace)
    return cleaned

@allow_guest_user
def render_cloze_exercise_freetext(request, template_id, gap_index, level):
    template = get_object_or_404(ClozeTemplate, id=template_id)
    topic = template.topic
    
    # Get user's progress for this topic
    progress = TopicProgress.objects.get_or_create(
        user=request.user,
        topic=topic
    )[0]
    
    # If streak is below 3, redirect to multiple choice
    if progress.streak < 3:
        return redirect('triangles:cloze', template_id=template_id, gap_index=gap_index, level=level)
    
    # Build cloze text with gap
    words = template.content.split()
    gap_index = int(gap_index)
    original_word = words[gap_index]
    punctuation_before = re.match(r'^[^\w]*', original_word).group()
    punctuation_after = re.search(r'[^\w]*$', original_word).group()
    words[gap_index] = f"{punctuation_before}_____{punctuation_after}"
    cloze_text = " ".join(words)
    correct_answer = clean_word(original_word)
    
    context = {
        'template_id': template_id,
        'gap_index': gap_index,
        'cloze_text': cloze_text,
        'correct_answer': correct_answer,
    }
    
    return render(request, 'triangles/cloze_freetext.html', context)

@allow_guest_user
def render_cloze_exercise(request, template_id, gap_index, level):
    template = get_object_or_404(ClozeTemplate, id=template_id)
    topic = template.topic
    
    # Get user's progress for this topic
    progress = TopicProgress.objects.get_or_create(
        user=request.user,
        topic=topic
    )[0]
    
    # If streak is 3 or higher, redirect to freetext
    if progress.streak >= 3:
        return redirect('triangles:cloze_freetext', template_id=template_id, gap_index=gap_index, level=level)

    # Build cloze text with gap
    words = template.content.split()
    gap_index = int(gap_index)
    original_word = words[gap_index]
    punctuation_before = re.match(r'^[^\w]*', original_word).group()
    punctuation_after = re.search(r'[^\w]*$', original_word).group()
    words[gap_index] = f"{punctuation_before}_____{punctuation_after}"
    cloze_text = " ".join(words)
    correct_answer = clean_word(original_word)

    # Use util to get a relevant distractor with matching case
    distractor_obj = get_random_relevant_distractor(correct_answer)
    distractor = distractor_obj.content if distractor_obj else "(keine)"
    answer_options = [correct_answer, distractor]

    context = {
        'template_id': template_id,
        'gap_index': gap_index,
        'cloze_text': cloze_text,
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

@csrf_exempt  # since only guest users, and for JS POST
@allow_guest_user
def submit_cloze_exercise(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    import json
    data = json.loads(request.body)
    user = request.user
    template_id = data.get('template_id')
    gap_index = data.get('gap_index')
    answer_given = data.get('answer_given')
    possible_answers = data.get('possible_answers')
    result = data.get('result')

    template = ClozeTemplate.objects.get(id=template_id)
    topic = template.topic

    # Upsert TopicProgress
    topic_progress, _ = TopicProgress.objects.get_or_create(user=user, topic=topic)
    # Upsert ClozeTemplateGapProgress
    gap_progress, _ = ClozeTemplateGapProgress.objects.get_or_create(user=user, template=template, gap_index=gap_index)

    if result == 'correct':
        topic_progress.streak += 1
        gap_progress.streak += 1
    else:
        topic_progress.streak = 0
        gap_progress.streak = 0
    topic_progress.save()
    gap_progress.save()

    # LearningEvent
    LearningEvent.objects.create(
        user=user,
        topic=topic,
        cloze_template=template,
        streak_before_answer=gap_progress.streak,  # after update, so this is the new streak
        possible_answers=possible_answers,
        answer_given=answer_given
    )
    return JsonResponse({}, status=204)