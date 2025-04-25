from django.urls import path
from withvideos.views.videos.list import LiveVideoListView
from withvideos.views.videos.detail import VideoDetailView
from withvideos.views.snippets.detail import SnippetDetailView
from django.shortcuts import redirect
from withvideos.models import Language

def redirect_to_preferred_language(request):
    # Get the preferred language from the request (set by middleware)
    preferred_lang = getattr(request, 'preferred_language', 'de')
    return redirect('withvideos:video_list', lang_code=preferred_lang)

app_name = 'withvideos'

urlpatterns = [
    path('', redirect_to_preferred_language, name='root'),
    path('videos/<str:lang_code>/', LiveVideoListView.as_view(), name='video_list'),
    path('videos/<str:lang_code>/<str:youtube_id>/', VideoDetailView.as_view(), name='video_detail'),
    path('snippets/<int:pk>/<str:mode>/', SnippetDetailView.as_view(), name='snippet_detail'),
] 