from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q

from german_with_videos.models import Video, Tag, TagType

@staff_member_required
def manage_tags(request, tag_id=None):
    """View to manage tags - add, edit, and list"""
    tag = None
    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            messages.error(request, "Tag not found.")
            return redirect('cms:german_with_videos:manage_tags')

    if request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')

        if not name:
            messages.error(request, "Tag name is required.")
            return redirect('cms:german_with_videos:manage_tags')

        try:
            if tag:
                # Update existing tag
                tag.name = name
                tag.type = type
                tag.save()
                messages.success(request, "Tag updated successfully.")
            else:
                # Create new tag
                Tag.objects.create(name=name, type=type)
                messages.success(request, "Tag created successfully.")
            return redirect('cms:german_with_videos:manage_tags')
        except Exception as e:
            messages.error(request, f"Error saving tag: {str(e)}")
            return redirect('cms:german_with_videos:manage_tags')

    # Get all tags for the list
    tags = Tag.objects.all().order_by('name')
    
    context = {
        'tag': tag,
        'tags': tags,
        'tag_types': TagType.choices
    }
    
    return render(request, 'cms/german_with_videos/tag_management.html', context)

@staff_member_required
@require_http_methods(["POST"])
def remove_tag(request, youtube_id, tag_id):
    """View to remove a tag from a video"""
    try:
        video = Video.objects.get(youtube_id=youtube_id)
        tag = Tag.objects.get(id=tag_id)
        video.tags.remove(tag)
        messages.success(request, f"Successfully removed tag '{tag.name}' from video.")
    except Video.DoesNotExist:
        messages.error(request, "Video not found.")
    except Tag.DoesNotExist:
        messages.error(request, "Tag not found.")
    except Exception as e:
        messages.error(request, f"Error removing tag: {str(e)}")
    
    return redirect('cms:german_with_videos:video_details', youtube_id=youtube_id)

@staff_member_required
@require_http_methods(["POST"])
def add_tag(request, youtube_id):
    """View to add a manual tag to a video"""
    try:
        video = Video.objects.get(youtube_id=youtube_id)
        tag_name = request.POST.get('tag_name', '').strip()
        
        if not tag_name:
            messages.error(request, "Tag name cannot be empty.")
            return redirect('cms:german_with_videos:video_details', youtube_id=youtube_id)
        
        # Get or create the tag (only manual tags can be created this way)
        tag, created = Tag.objects.get_or_create(
            name=tag_name.lower(),
            defaults={'type': TagType.MANUAL}
        )
        
        # Add the tag to the video
        video.tags.add(tag)
        
        if created:
            messages.success(request, f"Created and added new tag '{tag.name}' to video.")
        else:
            messages.success(request, f"Added existing tag '{tag.name}' to video.")
            
    except Video.DoesNotExist:
        messages.error(request, "Video not found.")
    except Exception as e:
        messages.error(request, f"Error adding tag: {str(e)}")
    
    return redirect('cms:german_with_videos:video_details', youtube_id=youtube_id)

@staff_member_required
def tag_autocomplete(request):
    """View to provide tag suggestions for autocomplete"""
    query = request.GET.get('q', '').strip().lower()
    
    if len(query) < 2:
        return JsonResponse({'tags': []})
    
    # Search for tags that start with the query
    tags = Tag.objects.filter(
        Q(name__istartswith=query) | Q(name__icontains=f" {query}")
    ).values('name')[:10]
    
    return JsonResponse({'tags': list(tags)})
