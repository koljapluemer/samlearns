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
    # Get total count of all videos
    total_videos = Video.objects.count()
    
    # Get counts for each status
    needs_review = Video.objects.filter(status=VideoStatus.NEEDS_REVIEW).count()
    shortlisted = Video.objects.filter(status=VideoStatus.SHORTLISTED).count()
    longlisted = Video.objects.filter(status=VideoStatus.LONGLISTED).count()
    not_relevant = Video.objects.filter(status=VideoStatus.NOT_RELEVANT).count()
    snippets_generated = Video.objects.filter(status=VideoStatus.SNIPPETS_GENERATED).count()
    snippets_and_translations_generated = Video.objects.filter(status=VideoStatus.SNIPPETS_AND_TRANSLATIONS_GENERATED).count()
    live = Video.objects.filter(status=VideoStatus.LIVE).count()
    blacklisted = Video.objects.filter(status=VideoStatus.BLACKLISTED).count()
    
    context = {
        'total_videos': total_videos,
        'needs_review': needs_review,
        'shortlisted': shortlisted,
        'longlisted': longlisted,
        'not_relevant': not_relevant,
        'snippets_generated': snippets_generated,
        'snippets_and_translations_generated': snippets_and_translations_generated,
        'live': live,
        'blacklisted': blacklisted,
    }
    return render(request, 'cms/german_with_videos/home.html', context)
