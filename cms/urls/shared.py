from django.urls import path
from cms.views.home import CMSHomeView

urlpatterns = [
    path('', CMSHomeView.as_view(), name='home'),
]
