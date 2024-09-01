from django.urls import path
from apps.macros_sheet.views import MealMacrosSheetDetailView

urlpatterns = [
    path('meal-macros-sheet/<uuid:pk>/', MealMacrosSheetDetailView.as_view(), name='meal_macros_sheet_detail'),
]
