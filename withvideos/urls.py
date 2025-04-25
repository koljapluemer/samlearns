from django.urls import path
from withvideos.views.videos.list import LiveVideoListView
from withvideos.views.videos.detail import VideoDetailView
from withvideos.views.snippets.detail import SnippetDetailView
from django.shortcuts import redirect

def redirect_to_german_videos(request):
    return redirect('withvideos:video_list', lang_code='de')

app_name = 'withvideos'

urlpatterns = [
    path('', redirect_to_german_videos, name='root'),
    path('videos/<str:lang_code>/', LiveVideoListView.as_view(), name='video_list'),
    path('videos/<str:lang_code>/<str:youtube_id>/', VideoDetailView.as_view(), name='video_detail'),
    path('snippets/<int:pk>/<str:mode>/', SnippetDetailView.as_view(), name='snippet_detail'),
] 