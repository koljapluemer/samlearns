from django.views.generic import TemplateView

class CMSHomeView(TemplateView):
    template_name = 'cms/home.html'
