from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.macros_sheet.views import MealMacrosSheetViewSet

router = DefaultRouter()
router.register(r'diets/(?P<diet_id>[0-9a-fA-F\-]+)/macros_sheets', MealMacrosSheetViewSet, basename='meal_macros_sheet')

urlpatterns = [
    path('', include(router.urls)),
]
