from django.urls import path, re_path
from .views import MacrosSheetListView, MacrosSheetDetailView

urlpatterns = [
    re_path(r'^diets/(?P<diet_id>[0-9a-fA-F\-]+)/macros_sheets/$', MacrosSheetListView.as_view(), name='macros_sheet_list'),
    re_path(r'^diets/(?P<diet_id>[0-9a-fA-F\-]+)/macros_sheets/(?P<macros_sheet_id>[0-9a-fA-F\-]+)/$', MacrosSheetDetailView.as_view(), name='macros_sheet_detail'),
]

