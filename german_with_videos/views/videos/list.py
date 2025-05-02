from django.views.generic import ListView
from german_with_videos.models import Video, VideoStatus
from django.http import HttpResponse

class LiveVideoListView(ListView):
    model = Video
    template_name = 'german_with_videos/videos/list.html'
    context_object_name = 'videos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        return Video.objects.filter(
            status=VideoStatus.LIVE
        ).order_by('-added_at')[:25]

    def render_to_response(self, context, **response_kwargs):
        return super().render_to_response(context, **response_kwargs)
