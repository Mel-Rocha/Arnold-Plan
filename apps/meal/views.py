from rest_framework import viewsets
from rest_framework.exceptions import NotFound

from apps.meal.models import Meal
from apps.diet.models import Diet
from config.urls import swagger_safe
from apps.meal.serializers import MealSerializer


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer

    @swagger_safe(Meal)
    def get_queryset(self):
        diet_id = self.kwargs.get('diet_id')

        try:
            diet = Diet.objects.get(id=diet_id)
        except Diet.DoesNotExist:
            raise NotFound(f'Diet with id {diet_id} does not exist')

        return Meal.objects.filter(diet=diet)

    def perform_create(self, serializer):
        diet_id = self.kwargs.get('diet_id')

        try:
            diet = Diet.objects.get(id=diet_id)
        except Diet.DoesNotExist:
            raise NotFound(f'Diet with id {diet_id} does not exist')

        serializer.context['diet_id'] = diet_id

        serializer.save(diet=diet)
