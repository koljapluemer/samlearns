from django.urls import path
from withvideos.views.videos.list import LiveVideoListView
from withvideos.views.videos.detail import VideoDetailView

app_name = 'withvideos'

urlpatterns = [
    path('ar/videos/', LiveVideoListView.as_view(), name='video_list_ar'),
    path('ar/videos/<str:youtube_id>/', VideoDetailView.as_view(), name='video_detail'),
] 