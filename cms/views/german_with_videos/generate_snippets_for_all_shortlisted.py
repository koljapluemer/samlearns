from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect

from youtube_transcript_api import YouTubeTranscriptApi
from german_with_videos.models import Video, VideoStatus, Snippet

@staff_member_required
@require_http_methods(["POST"])
def generate_snippets_for_all_shortlisted(request):
    """View to generate snippets for all shortlisted videos"""
    try:
        # Get all shortlisted videos
        videos = Video.objects.filter(status=VideoStatus.SHORTLISTED)
        processed_count = 0
        error_count = 0
        no_subtitles_count = 0
        error_videos = []
        
        for video in videos:
            try:
                # Get available languages if not already set
                if not video.available_subtitle_languages:
                    try:
                        available_languages = YouTubeTranscriptApi.list_transcripts(video.youtube_id)
                        video.available_subtitle_languages = [lang.language_code for lang in available_languages]
                        video.save()
                    except Exception:
                        video.available_subtitle_languages = []
                        video.save()
                
                # Try to get the transcript
                if video.available_subtitle_languages:
                    try:
                        transcript_list = YouTubeTranscriptApi.list_transcripts(video.youtube_id)
                        
                        # Get the first available transcript
                        transcript = transcript_list[0]
                        
                        transcript_data = transcript.fetch()
                        
                        # Delete existing snippets
                        video.snippets.all().delete()
                        
                        # Create new snippets
                        for index, segment in enumerate(transcript_data):
                            Snippet.objects.create(
                                video=video,
                                index=index,
                                content=segment.text,
                                start=segment.start,
                                duration=segment.duration
                            )
                        
                        # Update video status
                        video.status = VideoStatus.SNIPPETS_GENERATED
                        video.save()
                        processed_count += 1
                    except Exception as e:
                        error_count += 1
                        error_videos.append(f"{video.youtube_id} (Error: {str(e)})")
                else:
                    no_subtitles_count += 1
                    error_videos.append(f"{video.youtube_id} (No subtitles available)")
            except Exception as e:
                error_count += 1
                error_videos.append(f"{video.youtube_id} (Error: {str(e)})")
        
        if processed_count > 0:
            messages.success(request, f"Successfully generated snippets for {processed_count} videos.")
        if no_subtitles_count > 0:
            messages.warning(request, f"{no_subtitles_count} videos had no subtitles available.")
        if error_count > 0:
            messages.error(request, f"Failed to process {error_count} videos: {', '.join(error_videos)}")
            
    except Exception as e:
        messages.error(request, f"Error processing videos: {str(e)}")
    
    return redirect('cms:german_with_videos:list_all_videos')

