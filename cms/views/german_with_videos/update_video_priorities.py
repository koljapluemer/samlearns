from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.urls import reverse
from django.db import models

from german_with_videos.models import Video, VideoStatus

@staff_member_required
@require_http_methods(["POST"])
def update_video_priorities(request):
    """View to update priorities for all videos in the current filter"""
    try:
        # Get the current filter parameters
        status_filter = request.POST.get('status_filter', '')
        comment_filter = request.POST.get('comment_filter', '')
        
        # Get all videos
        videos = Video.objects.all()
        
        if status_filter:
            videos = videos.filter(status=status_filter)
        if comment_filter:
            videos = videos.filter(comment__icontains=comment_filter)
        
        # Get the action (increase or decrease)
        action = request.POST.get('action')
        
        # Update priorities
        if action == 'increase':
            videos.update(priority=models.F('priority') + 1)
            messages.success(request, "Successfully increased priority for all videos in the current filter.")
        elif action == 'decrease':
            videos.update(priority=models.F('priority') - 1)
            messages.success(request, "Successfully decreased priority for all videos in the current filter.")
        
    except Exception as e:
        messages.error(request, f"Error updating priorities: {str(e)}")
    
    # Redirect back to the list view with the same filters
    redirect_url = reverse('cms:german_with_videos:list_all_videos')
    if status_filter:
        redirect_url += f"?status={status_filter}"
    if comment_filter:
        redirect_url += f"{'&' if status_filter else '?'}comment={comment_filter}"
    
    return redirect(redirect_url)
