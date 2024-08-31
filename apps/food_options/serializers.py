import requests
from rest_framework import serializers

from apps.meal.models import Meal
from apps.food_options.models import FoodOptions


class FoodOptionsSerializer(serializers.ModelSerializer):
    food_description = serializers.CharField(write_only=True, required=False)
    food_id = serializers.IntegerField(write_only=True, required=False)
    quantity = serializers.FloatField()

    class Meta:
        model = FoodOptions
        fields = '__all__'
        extra_kwargs = {
            'meal': {'read_only': True}  # Meal is read-only and will be set automatically
        }

    def create(self, validated_data):
        meal_id = validated_data.pop('meal_id', None)
        food_description = validated_data.pop('food_description', None)
        food_id = validated_data.pop('food_id', None)
        quantity = validated_data.get('quantity')

        if not meal_id:
            raise serializers.ValidationError("Meal ID is required.")

        try:
            meal = Meal.objects.get(id=meal_id)
        except Meal.DoesNotExist:
            raise serializers.ValidationError(f"Meal with id {meal_id} does not exist.")

        if not food_id and not food_description:
            raise serializers.ValidationError("Either food_id or food_description is required.")

        # Use the existing endpoint to fetch and calculate the portion
        if food_id:
            response = requests.get(f'/taco/{food_id}/{quantity}/')
        else:
            response = requests.get(f'/taco/{food_description}/{quantity}/')

        if response.status_code != 200:
            raise serializers.ValidationError("Food not found or error in fetching food details.")

        food_data = response.json()
        validated_data['food'] = food_data['food_description']
        return FoodOptions.objects.create(meal=meal, **validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('meal', None)
        return super().update(instance, validated_data)
