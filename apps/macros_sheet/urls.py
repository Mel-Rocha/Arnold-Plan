from django.urls import path
from apps.macros_sheet.views import MealMacrosSheetDetailView, DietMacrosSheetDetailView

urlpatterns = [
    path('diet/<uuid:pk>/', DietMacrosSheetDetailView.as_view(), name='diet_macros_sheet_detail'),
    path('meal/<uuid:pk>/', MealMacrosSheetDetailView.as_view(), name='meal_macros_sheet_detail'),

]
