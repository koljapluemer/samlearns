from django.urls import path
from triangles.views.exercise_flow.redirect_to_next_exercise import redirect_to_next_exercise
from triangles.views.exercise_flow.redirect_to_next_exercise_of_type_cloze import redirect_to_next_exercise_of_type_cloze
from triangles.views.exercise_flow.redirect_to_next_exercise_of_type_image import redirect_to_next_exercise_of_type_image
from triangles.views.cloze.render_cloze_exercise_multiple_choice import render_cloze_exercise_multiple_choice
from triangles.views.cloze.render_cloze_exercise_freetext import render_cloze_exercise_freetext
from triangles.views.cloze.submit_cloze_exercise import submit_cloze_exercise

app_name = 'triangles'

urlpatterns = [
    path('', redirect_to_next_exercise, name='index'),
    path('cloze/multiple-choice/<int:template_id>/<int:gap_index>/<int:level>/',
         render_cloze_exercise_multiple_choice, name='cloze_multiple_choice'),
    path('cloze/freetext/<int:template_id>/<int:gap_index>/<int:level>/',
         render_cloze_exercise_freetext, name='cloze_freetext'),
    path('cloze/submit/', submit_cloze_exercise, name='cloze_submit'),
]
