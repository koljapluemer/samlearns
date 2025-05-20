from django.shortcuts import redirect
from triangles.interactors.user_dependent_learning_object.topic import get_due_topic
from triangles.interactors.user_dependent_learning_object.topic import user_should_get_image_instead_of_cloze_exercise
from guest_user.decorators import allow_guest_user
from django.contrib import messages
from triangles.views.exercise_flow import redirect_to_next_exercise_of_type_cloze, redirect_to_next_exercise_of_type_image

@allow_guest_user
def redirect_to_next_exercise(request):
    topic = get_due_topic(request.user)
    if not topic:
        messages.error(request, "No topics available")
        return redirect('triangles:index')

    should_get_image_instead_of_cloze_exercise = user_should_get_image_instead_of_cloze_exercise(request.user, topic)

    if should_get_image_instead_of_cloze_exercise:
        return redirect_to_next_exercise_of_type_image(request, topic)
    else:
        return redirect_to_next_exercise_of_type_cloze(request, topic)
