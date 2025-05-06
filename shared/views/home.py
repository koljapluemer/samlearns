from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['learning_apps'] = [
            {
                'name': 'Trees of Germany',
                'url': '/trees-of-germany/',
                'description': 'Learn about different tree species found in Germany',
                'icon': 'tree'
            },
            {
                'name': 'Uke Fingerpicking',
                'url': '/uke-fingerpicking/',
                'description': 'Learn ukulele fingerpicking techniques',
                'icon': 'music'
            }
        ]
        return context
