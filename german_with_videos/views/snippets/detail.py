from django.views.generic import DetailView
from german_with_videos.models import Snippet
import json
from random import shuffle

class SnippetDetailView(DetailView):
    model = Snippet
    template_name = 'german_with_videos/snippets/detail.html'
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
        
        # Get next snippet
        next_snippet = self.object.video.snippets.filter(index__gt=self.object.index).first()
        
        # Add to context as JSON
        context['words_json'] = json.dumps(words_data)
        context['snippet_data'] = json.dumps({
            'youtube_id': self.object.video.youtube_id,
            'start_time': self.object.start_time,
            'end_time': self.object.end_time,
            'next_snippet_url': next_snippet.get_absolute_url(mode='practice') if next_snippet else None
        })
        
        return context 