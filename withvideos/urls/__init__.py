from django.urls import include, path
from . import app, cms

app_name = 'withvideos'

urlpatterns = [
    path('', include(app.urlpatterns)),
    path('cms/', include((cms.urlpatterns, 'cms'), namespace='cms')),
]
