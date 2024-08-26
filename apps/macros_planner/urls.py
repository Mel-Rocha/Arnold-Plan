from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.macros_planner.views import MacrosPlannerViewSet

router = DefaultRouter()
router.register(r'', MacrosPlannerViewSet, basename='macros_planner')

urlpatterns = [
    path('', include(router.urls)),
]
