from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cms/', include('cms.urls')),
    path('trees-of-germany/', include('trees_of_germany.urls')),
    path('german-with-videos/', include('german_with_videos.urls')),
    path('uke-fingerpicking/', include('uke_fingerpicking.urls')),
]
