from django.urls import path
from triangles.views.exercise_flow import redirect_to_next_exercise, redirect_to_next_exercise_of_type_cloze, redirect_to_next_exercise_of_type_image
from triangles.views.cloze import render_cloze_exercise_multiple_choice, render_cloze_exercise_freetext, submit_cloze_exercise

app_name = 'triangles'

urlpatterns = [
    path('', redirect_to_next_exercise, name='index'),
    path('cloze/multiple-choice/<int:template_id>/<int:gap_index>/<int:level>/',
         render_cloze_exercise_multiple_choice, name='cloze_multiple_choice'),
    path('cloze/freetext/<int:template_id>/<int:gap_index>/<int:level>/',
         render_cloze_exercise_freetext, name='cloze_freetext'),
    path('cloze/submit/', submit_cloze_exercise, name='cloze_submit'),
]
