from django.urls import path
from uke_fingerpicking.views.app.tab_sheet_list import TabSheetListView
from uke_fingerpicking.views.app.tab_sheet_practice import (
    TabSheetPracticeSetupView,
    TabSheetPracticeActiveView,
    TabSheetPracticeResultsView
)

app_name = 'uke_fingerpicking'

urlpatterns = [
    path('', TabSheetListView.as_view(), name='tab_sheet_list'),
    path('practice/<int:pk>/', TabSheetPracticeSetupView.as_view(), name='tab_sheet_practice'),
    path('practice/<int:pk>/active/', TabSheetPracticeActiveView.as_view(), name='tab_sheet_practice_active'),
    path('practice/<int:pk>/results/', TabSheetPracticeResultsView.as_view(), name='tab_sheet_practice_results'),
]
