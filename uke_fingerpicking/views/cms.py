from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.forms.models import model_to_dict
from uke_fingerpicking.models import TabSheet, Beat
from django.utils.safestring import mark_safe
from django.contrib.auth.mixins import UserPassesTestMixin
import json

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class TabSheetListView(SuperuserRequiredMixin, ListView):
    model = TabSheet
    template_name = 'uke_fingerpicking/cms/tab_sheet_list.html'
    context_object_name = 'tab_sheets'

class TabSheetCreateView(SuperuserRequiredMixin, CreateView):
    model = TabSheet
    fields = ['title', 'artist']
    template_name = 'uke_fingerpicking/cms/tab_sheet_form.html'
    success_url = reverse_lazy('cms_tab_sheet_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Start with just one empty beat for new tab
        beats = [{'a': '', 'e': '', 'c': '', 'g': ''}]
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
        # Keep going until we find a beat that doesn't exist in the form
        while True:
            a = request.POST.get(f'beat_{idx}_a')
            e = request.POST.get(f'beat_{idx}_e')
            c = request.POST.get(f'beat_{idx}_c')
            g = request.POST.get(f'beat_{idx}_g')
            
            # If any of the fields don't exist, we've reached the end
            if None in (a, e, c, g):
                break
                
            beats.append({
                'a': a.strip() or '-',
                'e': e.strip() or '-',
                'c': c.strip() or '-',
                'g': g.strip() or '-'
            })
            idx += 1
        return beats

class TabSheetUpdateView(SuperuserRequiredMixin, UpdateView):
    model = TabSheet
    fields = ['title', 'artist']
    template_name = 'uke_fingerpicking/cms/tab_sheet_form.html'
    success_url = reverse_lazy('cms_tab_sheet_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Load all existing beats
        beats = list(
            Beat.objects.filter(tab_sheet=self.object).order_by('index').values('a', 'e', 'c', 'g')
        )
        # If no beats exist, start with one empty beat
        if not beats:
            beats = [{'a': '', 'e': '', 'c': '', 'g': ''}]
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
        # Keep going until we find a beat that doesn't exist in the form
        while True:
            a = request.POST.get(f'beat_{idx}_a')
            e = request.POST.get(f'beat_{idx}_e')
            c = request.POST.get(f'beat_{idx}_c')
            g = request.POST.get(f'beat_{idx}_g')
            
            # If any of the fields don't exist, we've reached the end
            if None in (a, e, c, g):
                break
                
            beats.append({
                'a': a.strip() or '-',
                'e': e.strip() or '-',
                'c': c.strip() or '-',
                'g': g.strip() or '-'
            })
            idx += 1
        return beats
