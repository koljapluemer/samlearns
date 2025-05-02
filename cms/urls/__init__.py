from django.urls import path, include

app_name = 'cms'

urlpatterns = [
    path('german-with-videos/', include('cms.urls.german_with_videos', namespace='german_with_videos')),
]
