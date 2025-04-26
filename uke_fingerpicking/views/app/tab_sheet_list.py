from django.views.generic import ListView
from uke_fingerpicking.models import TabSheet

class TabSheetListView(ListView):
    model = TabSheet
    template_name = 'uke_fingerpicking/app/tab_sheet_list.html'
    context_object_name = 'tab_sheets'
    ordering = ['title']
