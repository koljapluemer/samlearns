from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect

from german_with_videos.models import Video, VideoStatus

@staff_member_required
@require_http_methods(["POST"])
def mark_videos_without_german_subtitles(request):
    """View to mark videos without target language subtitles as not relevant"""
    try:
        # Get all videos that haven't been checked for subtitles and aren't marked as not relevant
        videos = Video.objects.filter(
            checked_for_relevant_subtitles=False
        ).exclude(
            status=VideoStatus.NOT_RELEVANT
        )
        
        marked_count = 0
        
        for video in videos:
            # Check if video has subtitles
            has_subtitles = bool(video.available_subtitle_languages)
            
            if not has_subtitles:
                video.status = VideoStatus.NOT_RELEVANT
                video.checked_for_relevant_subtitles = True
                video.save()
                marked_count += 1
        
        messages.success(request, f"Successfully marked {marked_count} videos without subtitles as not relevant.")
    except Exception as e:
        messages.error(request, f"Error marking videos: {str(e)}")
    
    return redirect('cms:german_with_videos:list_all_videos')
