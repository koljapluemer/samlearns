from django.urls import path
from . import views
from .views import submit_cloze_exercise

app_name = 'triangles'

urlpatterns = [
    path('', views.redirect_to_next_exercise, name='index'),
    path('cloze/<int:template_id>/<int:gap_index>/<int:level>/', 
         views.render_cloze_exercise, name='cloze'),
    path('cloze/freetext/<int:template_id>/<int:gap_index>/<int:level>/',
         views.render_cloze_exercise_freetext, name='cloze_freetext'),
    path('cloze/submit/', submit_cloze_exercise, name='cloze_submit'),
]
