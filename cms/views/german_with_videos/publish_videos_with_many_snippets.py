from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.db import models

from german_with_videos.models import Video, VideoStatus

@staff_member_required
@require_http_methods(["POST"])
def publish_videos_with_many_snippets(request):
    """View to publish videos that have more than 5 snippets and are ready for publishing"""
    try:
        # Get videos with more than 5 snippets and status SNIPPETS_AND_TRANSLATIONS_GENERATED
        videos = Video.objects.filter(
            status=VideoStatus.SNIPPETS_AND_TRANSLATIONS_GENERATED
        ).annotate(
            snippet_count=models.Count('snippets')
        ).filter(
            snippet_count__gt=5
        )
        
        count = videos.count()
        videos.update(status=VideoStatus.LIVE)
        
        messages.success(request, f"Successfully published {count} videos with more than 5 snippets.")
    except Exception as e:
        messages.error(request, f"Error publishing videos: {str(e)}")
    
    return redirect('cms:german_with_videos:actions')

