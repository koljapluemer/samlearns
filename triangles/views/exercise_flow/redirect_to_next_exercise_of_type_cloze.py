from django.shortcuts import redirect
from triangles.models import Topic, ClozeTemplateGapProgress
from triangles.interactors.cloze.get_random_cloze_template_for_topic import get_random_cloze_template_for_topic
from triangles.interactors.user_dependent_learning_object.cloze.get_due_gap_index_for_cloze_template import get_due_gap_index_for_cloze_template


def redirect_to_next_exercise_of_type_cloze(request, topic: Topic):
    # Get random cloze template from topic
    template = get_random_cloze_template_for_topic(topic)
    if not template:
        return redirect('triangles:index')

    # Get due gap index
    gap_index = get_due_gap_index_for_cloze_template(request.user, template)

    # Check if user has a fitting ClozeTemplateGapProgress
    gap_progress = ClozeTemplateGapProgress.objects.filter(
        user=request.user,
        template=template,
        gap_index=gap_index
    ).first()

    # If streak is 3 or higher, redirect to freetext, otherwise multiple choice
    if gap_progress and gap_progress.streak >= 3:
        return redirect('triangles:cloze_freetext', template_id=template.id, gap_index=gap_index, level=1)
    else:
        return redirect('triangles:cloze_multiple_choice', template_id=template.id, gap_index=gap_index, level=1)
