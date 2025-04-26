from django.urls import path, include

urlpatterns = [
    path('', include('uke_fingerpicking.urls.app')),
    path('cms/', include('uke_fingerpicking.urls.cms')),
]
