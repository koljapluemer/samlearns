from django.urls import path
from withvideos.views.videos.list import LiveVideoListView

app_name = 'withvideos'

urlpatterns = [
    path('ar/videos/', LiveVideoListView.as_view(), name='video_list_ar'),
] 