from django.shortcuts import get_object_or_404
from triangles.models import ClozeTemplate
from guest_user.decorators import allow_guest_user
from django.shortcuts import render, redirect, get_object_or_404
from triangles.interactors.cloze import generate_cloze_exercise

@allow_guest_user
def render_cloze_exercise_freetext(request, template_id, gap_index, level):
    # render a cloze exercise with a freetext input field
    template = get_object_or_404(ClozeTemplate, id=template_id)
    topic = template.topic
    
    # Get the correct answer from the template
    correct_answer = template.get_gap_at_index(gap_index)
    
    # Generate cloze text with gap
    cloze_result = generate_cloze_exercise(template.content, correct_answer)
    cloze_text = cloze_result['template']
    correct_answer = cloze_result['answer']
    
    context = {
        'template_id': template_id,
        'gap_index': gap_index,
        'cloze_text': cloze_text,
        'correct_answer': correct_answer,
    }
    
    return render(request, 'triangles/cloze_freetext.html', context)