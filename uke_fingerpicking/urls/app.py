from django.urls import path
from uke_fingerpicking.views.app.tab_sheet_list import TabSheetListView
from uke_fingerpicking.views.app.tab_sheet_practice import TabSheetPracticeView

app_name = 'uke_fingerpicking'

urlpatterns = [
    path('', TabSheetListView.as_view(), name='tab_sheet_list'),
    path('practice/<int:pk>/', TabSheetPracticeView.as_view(), name='tab_sheet_practice'),
]
