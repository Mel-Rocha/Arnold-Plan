from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.meal.views import MealViewSet

router = DefaultRouter()
router.register(r'diets/(?P<diet_id>[0-9a-f-]+)/meals', MealViewSet, basename='meal')

urlpatterns = [
    path('', include(router.urls)),
]
