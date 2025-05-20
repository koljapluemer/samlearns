from guest_user.decorators import allow_guest_user
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import json

from triangles.models import ClozeTemplate, Topic, TopicProgress, ClozeTemplateGapProgress, LearningEvent, Distractor





@csrf_exempt  # since only guest users, and for JS POST
@allow_guest_user
def submit_cloze_exercise(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    
    user = request.user
    template_id = request.POST.get('template_id')
    gap_index = request.POST.get('gap_index')
    answer_given = request.POST.get('answer_given')
    possible_answers = json.loads(request.POST.get('possible_answers', '[]'))
    result = request.POST.get('result')

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
    
    # Redirect to next exercise
    return redirect('triangles:index')