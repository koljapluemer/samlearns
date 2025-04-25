from django.urls import path
from .views.home import home

app_name = 'trees_of_germany'

urlpatterns = [
    path('', home, name='home'),
] 