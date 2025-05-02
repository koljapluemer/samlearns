from django.views.generic import DetailView
from german_with_videos.models import Video

class VideoDetailView(DetailView):
    model = Video
    template_name = 'german_with_videos/videos/detail.html'
    slug_field = 'youtube_id'
    slug_url_kwarg = 'youtube_id'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_snippet = self.object.snippets.first()
        if first_snippet:
            context['first_snippet_practice_url'] = first_snippet.get_absolute_url(mode='practice')
        return context 