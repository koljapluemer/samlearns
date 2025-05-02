from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'german_with_videos/home.html'
