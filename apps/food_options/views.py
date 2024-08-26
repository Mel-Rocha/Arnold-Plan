from rest_framework import viewsets
from django_rest_passwordreset import serializers

from apps.food_options.models import FoodOptions
from apps.food_options.serializers import FoodOptionsSerializer


class FoodOptionsViewSet(viewsets.ModelViewSet):
    queryset = FoodOptions.objects.all()
    serializer_class = FoodOptionsSerializer

    def perform_create(self, serializer):
        meal_id = self.kwargs.get('meal_id')
        if not meal_id:
            raise serializers.ValidationError("Meal ID is required.")
        serializer.save(meal_id=meal_id)
