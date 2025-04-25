from django.views.generic import DetailView
from withvideos.models import Snippet
import json
from random import shuffle

class SnippetDetailView(DetailView):
    model = Snippet
    template_name = 'withvideos/snippets/detail.html'
    context_object_name = 'snippet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mode'] = self.kwargs.get('mode', 'practice')  # Default to practice mode
        
        # Prepare words data for Alpine.js
        words_data = []
        for word in self.object.words.all():
            words_data.append({
                'id': word.id,
                'original_word': word.original_word,
                'meanings': [meaning.en for meaning in word.meanings.all()]
            })
        
        # Randomize the order
        shuffle(words_data)
        
        # Add to context as JSON
        context['words_json'] = json.dumps(words_data)
        
        return context 