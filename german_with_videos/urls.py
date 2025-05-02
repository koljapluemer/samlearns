from django.urls import path
from german_with_videos.views.videos.list import LiveVideoListView
from german_with_videos.views.videos.detail import VideoDetailView
from german_with_videos.views.snippets.detail import SnippetDetailView
from german_with_videos.views.home import HomeView

app_name = 'german_with_videos'

urlpatterns = [
    path('', HomeView.as_view(), name='root'),
    path('videos/', LiveVideoListView.as_view(), name='video_list'),
    path('videos/<str:youtube_id>/', VideoDetailView.as_view(), name='video_detail'),
    path('snippets/<int:pk>/<str:mode>/', SnippetDetailView.as_view(), name='snippet_detail'),
] 