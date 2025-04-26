from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.forms.models import model_to_dict
from uke_fingerpicking.models import TabSheet, Beat
from django.utils.safestring import mark_safe
import json

class TabSheetListView(ListView):
    model = TabSheet
    template_name = 'uke_fingerpicking/tab_sheet_list.html'
    context_object_name = 'tab_sheets'

class TabSheetCreateView(CreateView):
    model = TabSheet
    fields = ['title', 'artist']
    template_name = 'uke_fingerpicking/tab_sheet_form.html'
    success_url = reverse_lazy('cms_tab_sheet_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 10 empty beats for new tab
        beats = [
            {'a': '', 'e': '', 'c': '', 'g': ''} for _ in range(10)
        ]
        context['beats_json'] = mark_safe(json.dumps(beats))
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self._save_beats(self.object, self.request)
        return response

    def _save_beats(self, tab_sheet, request):
        # Remove existing beats (should be none for create)
        Beat.objects.filter(tab_sheet=tab_sheet).delete()
        beats = self._parse_beats_from_post(request)
        for idx, beat in enumerate(beats):
            Beat.objects.create(
                tab_sheet=tab_sheet,
                index=idx,
                a=beat['a'],
                e=beat['e'],
                c=beat['c'],
                g=beat['g'],
            )

    def _parse_beats_from_post(self, request):
        beats = []
        idx = 0
        while True:
            a = request.POST.get(f'beat_{idx}_a', '').strip() or '-'
            e = request.POST.get(f'beat_{idx}_e', '').strip() or '-'
            c = request.POST.get(f'beat_{idx}_c', '').strip() or '-'
            g = request.POST.get(f'beat_{idx}_g', '').strip() or '-'
            if all(x == '-' for x in (a, e, c, g)):
                break  # stop at first all-empty beat (trailing empty columns)
            beats.append({'a': a, 'e': e, 'c': c, 'g': g})
            idx += 1
        return beats

class TabSheetUpdateView(UpdateView):
    model = TabSheet
    fields = ['title', 'artist']
    template_name = 'uke_fingerpicking/tab_sheet_form.html'
    success_url = reverse_lazy('cms_tab_sheet_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        beats = list(
            Beat.objects.filter(tab_sheet=self.object).order_by('index').values('a', 'e', 'c', 'g')
        )
        if not beats:
            beats = [{'a': '', 'e': '', 'c': '', 'g': ''} for _ in range(10)]
        context['beats_json'] = mark_safe(json.dumps(beats))
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self._save_beats(self.object, self.request)
        return response

    def _save_beats(self, tab_sheet, request):
        Beat.objects.filter(tab_sheet=tab_sheet).delete()
        beats = self._parse_beats_from_post(request)
        for idx, beat in enumerate(beats):
            Beat.objects.create(
                tab_sheet=tab_sheet,
                index=idx,
                a=beat['a'],
                e=beat['e'],
                c=beat['c'],
                g=beat['g'],
            )

    def _parse_beats_from_post(self, request):
        beats = []
        idx = 0
        while True:
            a = request.POST.get(f'beat_{idx}_a', '').strip() or '-'
            e = request.POST.get(f'beat_{idx}_e', '').strip() or '-'
            c = request.POST.get(f'beat_{idx}_c', '').strip() or '-'
            g = request.POST.get(f'beat_{idx}_g', '').strip() or '-'
            if all(x == '-' for x in (a, e, c, g)):
                break
            beats.append({'a': a, 'e': e, 'c': c, 'g': g})
            idx += 1
        return beats
