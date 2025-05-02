from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.db import models

from german_with_videos.models import Video, VideoStatus

@staff_member_required
def actions(request):
    """View for the actions page"""
    unchecked_count = Video.objects.filter(
        checked_for_relevant_subtitles=False
    ).exclude(
        status=VideoStatus.NOT_RELEVANT
    ).count()
    context = {
        'unchecked_count': unchecked_count
    }
    return render(request, 'cms/german_with_videos/actions.html', context)


@staff_member_required
@never_cache
def cms_home(request):
    """CMS home page showing overview of video statuses"""
    status_counts = Video.objects.values('status').annotate(count=models.Count('id'))
    status_data = {item['status']: item['count'] for item in status_counts}
    
    context = {
        'status_data': status_data,
    }
    return render(request, 'cms/german_with_videos/home.html', context)
