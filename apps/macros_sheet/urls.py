from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.macros_sheet.views import MealMacrosSheetViewSet, DietMacrosSheetViewSet

router = DefaultRouter()
router.register(r'meal-macros-sheets', MealMacrosSheetViewSet, basename='meal-macros-sheet')
router.register(r'diet-macros-sheets', DietMacrosSheetViewSet, basename='diet-macros-sheet')

urlpatterns = [
    path('', include(router.urls)),
]