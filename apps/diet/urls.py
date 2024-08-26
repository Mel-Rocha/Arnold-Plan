from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.diet.views import DietViewSet

router = DefaultRouter()
router.register(r'macros_planner/(?P<macros_planner_id>[0-9a-f-]+)/diets', DietViewSet, basename='diet')

urlpatterns = [
    path('', include(router.urls)),
]