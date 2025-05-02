from django.urls import path
from shared.views.home import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
