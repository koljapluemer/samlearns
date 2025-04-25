from django.views.generic import ListView
from withvideos.models import Video, VideoStatus, Language
from django.shortcuts import redirect

class LiveVideoListView(ListView):
    model = Video
    template_name = 'withvideos/videos/list.html'
    context_object_name = 'videos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.objects.all()
        context['current_lang'] = self.kwargs.get('lang_code')
        return context
    
    def get_queryset(self):
        lang_code = self.kwargs.get('lang_code')
        try:
            language = Language.objects.get(code=lang_code)
            return Video.objects.filter(
                status=VideoStatus.LIVE,
                language=language
            ).order_by('-added_at')[:25]
        except Language.DoesNotExist:
            return Video.objects.none()
    
    def get(self, request, *args, **kwargs):
        if not self.kwargs.get('lang_code'):
            # Redirect to default language if none specified
            default_lang = Language.objects.first()
            if default_lang:
                return redirect('withvideos:video_list', lang_code=default_lang.code)
        return super().get(request, *args, **kwargs)
