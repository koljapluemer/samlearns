from django.shortcuts import render, redirect
from django.contrib import messages
from guest_user.decorators import allow_guest_user
import string

from triangles.models import ClozeTemplate
from triangles.utils import get_due_topic, get_due_gap_index_for_cloze_template

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
    
    # Split content into words and create cloze text
    words = template.content.split()
    words[gap_index] = "_____"
    cloze_text = " ".join(words)
    
    if request.method == 'POST':
        user_answer = clean_word(request.POST.get('answer', ''))
        correct_word = clean_word(words[gap_index])
        
        if user_answer == correct_word:
            messages.success(request, "Correct!")
        else:
            messages.error(request, f"Wrong! The correct answer was: {correct_word}")
    
    context = {
        'cloze_text': cloze_text,
        'template_id': template_id,
        'gap_index': gap_index,
        'level': level,
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