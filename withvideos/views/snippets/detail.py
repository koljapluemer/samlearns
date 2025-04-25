from django.views.generic import DetailView
from withvideos.models import Snippet

class SnippetDetailView(DetailView):
    model = Snippet
    template_name = 'withvideos/snippets/detail.html'
    context_object_name = 'snippet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mode'] = self.kwargs.get('mode', 'practice')  # Default to practice mode
        return context 