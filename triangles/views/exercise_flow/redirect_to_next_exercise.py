from django.shortcuts import redirect
from django.contrib import messages
import random
import time
from triangles.interactors.user_dependent_learning_object.topic.get_due_topic import get_due_topic
from triangles.models import Topic
from guest_user.decorators import allow_guest_user

@allow_guest_user
def redirect_to_next_exercise(request):
    # Check if all congruence theorem topics have a streak of 5
    congruence_theorems = Topic.objects.filter(is_congruence_theorem=True)
    all_topics_learned = True
    
    for topic in congruence_theorems:
        if topic.get_streak(request.user) < 5:
            all_topics_learned = False
            break
    
    if all_topics_learned:
        return redirect('triangles:all_learned')
    
    # Seed random with current time to ensure different results
    random.seed(time.time())
    
    topic = get_due_topic(request.user)
    if not topic:
        messages.error(request, "No topics available")
        return redirect('triangles:index')

    # Try a different approach to random selection
    rand_val = random.random()
    print(f"Random value: {rand_val}")  # Debug print
    
    if rand_val < 0.5:
        print("redirecting to identify theorem exercise")
        return redirect('triangles:next_theorem', topic_id=topic.id)
    else:
        print("redirecting to cloze exercise")
        return redirect('triangles:next_cloze', topic_id=topic.id)
