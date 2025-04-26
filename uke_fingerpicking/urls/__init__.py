from django.urls import path, include

urlpatterns = [
    path('cms/', include('uke_fingerpicking.urls.cms')),
]
