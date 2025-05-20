from django.shortcuts import redirect
from django.contrib import messages
import random
import time
from triangles.interactors.user_dependent_learning_object.topic.get_due_topic import get_due_topic
from triangles.views.exercise_flow.redirect_to_next_exercise_of_type_cloze import redirect_to_next_exercise_of_type_cloze
from triangles.views.exercise_flow.redirect_to_next_exercise_of_type_identify_theorem import redirect_to_next_exercise_of_type_identify_theorem
from guest_user.decorators import allow_guest_user

@allow_guest_user
def redirect_to_next_exercise(request):
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
        return redirect_to_next_exercise_of_type_identify_theorem(request, topic)
    else:
        print("redirecting to cloze exercise")
        return redirect_to_next_exercise_of_type_cloze(request, topic)
