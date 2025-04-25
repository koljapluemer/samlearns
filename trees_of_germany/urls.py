from django.urls import path
from .views.home import home
from .views.learn_trees import learn_trees

app_name = 'trees_of_germany'

urlpatterns = [
    path('', home, name='home'),
    path('learn/', learn_trees, name='learn_trees'),
] 