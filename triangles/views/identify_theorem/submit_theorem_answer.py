from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
import random

from triangles.models import Topic, TopicProgress, LearningEvent

POSITIVE_MESSAGES = [
    'Sehr gut!',
    'Stark!',
    'Super gemacht!',
    'Perfekt!',
    'Ausgezeichnet!'
]

@csrf_exempt  # for JS POST
@login_required
def submit_theorem_answer(request):
    if request.method == 'POST':
        selected_theorem = request.POST.get('selected_theorem')
        correct_theorem = request.POST.get('correct_theorem')
        result = request.POST.get('result')
        user = request.user
        
        is_correct = selected_theorem == correct_theorem
        # Get the topic for the correct theorem
        try:
            topic = Topic.objects.get(name__iexact=correct_theorem, is_congruence_theorem=True)
        except Topic.DoesNotExist:
            return HttpResponse('Topic not found', status=404)
        
        # Upsert TopicProgress
        topic_progress, _ = TopicProgress.objects.get_or_create(user=user, topic=topic)
        if result == 'correct':
            topic_progress.streak += 1
            messages.success(request, random.choice(POSITIVE_MESSAGES))
        else:
            topic_progress.streak = 0
        topic_progress.save()
        
        # Record LearningEvent
        possible_answers = ['sss', 'ssw', 'sws', 'wsw']
        LearningEvent.objects.create(
            user=user,
            topic=topic,
            exercise_type='identify_theorem',
            streak_before_answer=topic_progress.streak,  # after update
            possible_answers=possible_answers,
            answer_given=selected_theorem
        )
        
        # Redirect to next exercise
        return redirect('triangles:index')
    
    return HttpResponse('Invalid request method', status=400) 