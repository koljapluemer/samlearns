from django.shortcuts import redirect

from triangles.models import Topic


def redirect_to_next_exercise_of_type_identify_theorem(request, topic):
    # For now, just redirect to the identify theorem exercise
    # In the future, we might want to add topic-specific logic here
    return redirect('triangles:identify_theorem')
