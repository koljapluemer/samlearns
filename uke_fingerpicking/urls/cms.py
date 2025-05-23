from django.contrib import admin
from django.urls import path, include
from uke_fingerpicking.views.cms import TabSheetListView, TabSheetCreateView, TabSheetUpdateView

app_name = 'uke_fingerpicking_cms'

urlpatterns = [
    path('tabs/', TabSheetListView.as_view(), name='tab_sheet_list'),
    path('tabs/add/', TabSheetCreateView.as_view(), name='tab_sheet_add'),
    path('tabs/<int:pk>/edit/', TabSheetUpdateView.as_view(), name='tab_sheet_edit'),
]