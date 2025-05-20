from django.shortcuts import redirect

from triangles.models import Topic


def redirect_to_next_exercise_of_type_cloze(request, topic: Topic):
    # not yet implemented, redirect to index
    return redirect('triangles:index')
