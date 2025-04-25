from django.views.generic import ListView
from withvideos.models import Video, VideoStatus

class LiveVideoListView(ListView):
    model = Video
    template_name = 'withvideos/videos/list.html'
    context_object_name = 'videos'
    
    def get_queryset(self):
        return Video.objects.filter(
            status=VideoStatus.LIVE
        ).order_by('-added_at')[:25]
