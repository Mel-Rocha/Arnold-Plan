from rest_framework import serializers

from apps.meal.models import Meal
from apps.food_options.models import FoodOptions


class FoodOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodOptions
        fields = '__all__'
        extra_kwargs = {
            'meal': {'read_only': True}  # Meal is read-only and will be set automatically
        }

    def create(self, validated_data):
        meal_id = validated_data.pop('meal_id', None)
        if not meal_id:
            raise serializers.ValidationError("Meal ID is required.")

        try:
            meal = Meal.objects.get(id=meal_id)
        except Meal.DoesNotExist:
            raise serializers.ValidationError(f"Meal with id {meal_id} does not exist.")

        return FoodOptions.objects.create(meal=meal, **validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('meal', None)
        return super().update(instance, validated_data)
