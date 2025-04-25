from django.views.generic import DetailView
from withvideos.models import Video

class VideoDetailView(DetailView):
    model = Video
    template_name = 'withvideos/videos/detail.html'
    slug_field = 'youtube_id'
    slug_url_kwarg = 'youtube_id'
    context_object_name = 'video' 