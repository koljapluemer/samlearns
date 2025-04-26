from django.views.generic import DetailView
from uke_fingerpicking.models import TabSheet, Beat
from django.utils.safestring import mark_safe
import json

class TabSheetPracticeView(DetailView):
    model = TabSheet
    template_name = 'uke_fingerpicking/app/tab_sheet_practice.html'
    context_object_name = 'tab_sheet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all beats ordered by index
        beats = list(Beat.objects.filter(tab_sheet=self.object).order_by('index').values('a', 'e', 'c', 'g'))
        context['beats_json'] = mark_safe(json.dumps(beats))
        return context 