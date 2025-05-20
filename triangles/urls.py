from django.urls import path
from . import views

app_name = 'triangles'

urlpatterns = [
    path('', views.redirect_to_next_exercise, name='index'),
    path('cloze/<int:template_id>/<int:gap_index>/<int:level>/', 
         views.render_cloze_exercise, name='cloze'),
]
