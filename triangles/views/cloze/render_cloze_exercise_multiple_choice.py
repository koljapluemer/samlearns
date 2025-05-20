from django.shortcuts import get_object_or_404
from triangles.interactors.distractor import get_random_relevant_distractor
from triangles.models import ClozeTemplate
from guest_user.decorators import allow_guest_user
from django.shortcuts import render, redirect, get_object_or_404

@allow_guest_user
def render_cloze_exercise_multiple_choice(request, template_id, gap_index, level):
    template = get_object_or_404(ClozeTemplate, id=template_id)
    topic = template.topic
    
   # Implement:Build cloze text with gap
    # use generate_cloze_exercise()
    

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
    
    return render(request, 'triangles/cloze_multiple_choice.html', context)