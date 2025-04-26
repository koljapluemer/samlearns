from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trees-of-germany/', include('trees_of_germany.urls')),
    path('withvideos/', include('withvideos.urls')),
    path('uke-fingerpicking/', include('uke_fingerpicking.urls')),
]
