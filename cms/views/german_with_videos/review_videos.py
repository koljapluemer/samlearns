from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.core.paginator import Paginator

from german_with_videos.models import Video, VideoStatus

@staff_member_required
@never_cache
def review_videos(request):
    """Review videos that need attention"""
    videos = Video.objects.filter(
        status=VideoStatus.NEEDS_REVIEW
    ).order_by('-priority', '-added_at')
    
    paginator = Paginator(videos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'videos': page_obj,
    }
    return render(request, 'cms/german_with_videos/review.html', context)
