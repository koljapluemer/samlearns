from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.core.paginator import Paginator

from german_with_videos.models import Video, VideoStatus

@staff_member_required
@never_cache
def list_all_videos(request):
    """List all videos with filtering options"""
    videos = Video.objects.all().order_by('-added_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        videos = videos.filter(status=status)
    
    paginator = Paginator(videos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'videos': page_obj,
        'status_choices': VideoStatus.choices,
    }
    return render(request, 'cms/german_with_videos/list.html', context)

