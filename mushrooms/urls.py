from django.urls import path
from .views.home import home
from .views.learn import learn

app_name = 'mushrooms'

urlpatterns = [
    path('', home, name='home'),
    path('learn/', learn, name='learn'),
] 