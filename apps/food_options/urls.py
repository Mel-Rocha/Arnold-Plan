from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.food_options.views import FoodOptionsViewSet

router = DefaultRouter()
router.register(
    r'macros-planner/(?P<macros_planner_id>[0-9a-f-]+)/diets/(?P<diet_id>[0-9a-f-]+)/meals/(?P'
    r'<meal_id>[0-9a-f-]+)/food-options',
    FoodOptionsViewSet,
    basename='food-options'
)

urlpatterns = [
    path('', include(router.urls)),
]
