from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MacrosSheetViewSet

router = DefaultRouter()
router.register(r'diets/(?P<diet_id>[0-9a-fA-F\-]+)/macros_sheets', MacrosSheetViewSet, basename='macros_sheet')

urlpatterns = [
    path('', include(router.urls)),
]
