from rest_framework import viewsets
from rest_framework.exceptions import NotFound

from apps.meal.models import Meal
from apps.diet.models import Diet
from apps.meal.serializers import MealSerializer
from apps.macros_planner.models import MacrosPlanner
from config.urls import swagger_safe


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer

    @swagger_safe(Meal)
    def get_queryset(self):
        macros_planner_id = self.kwargs.get('macros_planner_id')
        diet_id = self.kwargs.get('diet_id')

        try:
            macros_planner = MacrosPlanner.objects.get(id=macros_planner_id)
        except MacrosPlanner.DoesNotExist:
            raise NotFound(f'MacrosPlanner with id {macros_planner_id} does not exist')

        try:
            diet = Diet.objects.get(id=diet_id, macros_planner=macros_planner)
        except Diet.DoesNotExist:
            raise NotFound(f'Diet with id {diet_id} does not exist or does not belong to MacrosPlanner with id '
                           f'{macros_planner_id}')

        return Meal.objects.filter(diet=diet)

    def perform_create(self, serializer):
        macros_planner_id = self.kwargs.get('macros_planner_id')
        diet_id = self.kwargs.get('diet_id')

        try:
            MacrosPlanner.objects.get(id=macros_planner_id)
        except MacrosPlanner.DoesNotExist:
            raise NotFound(f'MacrosPlanner with id {macros_planner_id} does not exist')

        try:
            diet = Diet.objects.get(id=diet_id, macros_planner__id=macros_planner_id)
        except Diet.DoesNotExist:
            raise NotFound(f'Diet with id {diet_id} does not exist or does not belong to MacrosPlanner with id '
                           f'{macros_planner_id}')

        serializer.context['diet_id'] = diet_id

        serializer.save(diet=diet)
