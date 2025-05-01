from django.views.generic import DetailView, TemplateView
from uke_fingerpicking.models import TabSheet, Beat
from django.utils.safestring import mark_safe
import json

class TabSheetPracticeSetupView(DetailView):
    model = TabSheet
    template_name = 'uke_fingerpicking/app/tab_sheet_practice_setup.html'
    context_object_name = 'tab_sheet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        beats = list(Beat.objects.filter(tab_sheet=self.object).order_by('index').values('a', 'e', 'c', 'g'))
        context['beats_json'] = json.dumps(beats)
        return context

class TabSheetPracticeActiveView(DetailView):
    model = TabSheet
    template_name = 'uke_fingerpicking/app/tab_sheet_practice_active.html'
    context_object_name = 'tab_sheet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        beats = list(Beat.objects.filter(tab_sheet=self.object).order_by('index').values('a', 'e', 'c', 'g'))
        context['beats_json'] = json.dumps(beats)
        context['initial_bpm'] = self.request.GET.get('bpm', 40)
        context['tab_sheet_data'] = {
            'id': self.object.id,
            'title': self.object.title,
            'artist': self.object.artist
        }
        return context

class TabSheetPracticeResultsView(DetailView):
    model = TabSheet
    template_name = 'uke_fingerpicking/app/tab_sheet_practice_results.html'
    context_object_name = 'tab_sheet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tab_sheet_data'] = {
            'id': self.object.id,
            'title': self.object.title,
            'artist': self.object.artist
        }
        return context 