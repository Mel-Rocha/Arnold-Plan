from rest_framework import serializers

from apps.meal.models import Meal
from apps.diet.models import Diet
from apps.meal.serializers import MealSerializer
from apps.food_options.models import FoodOptions
from apps.macros_planner.models import MacrosPlanner


class DietSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, required=False)

    class Meta:
        model = Diet
        fields = '__all__'
        extra_kwargs = {
            'macros_planner': {'read_only': True}
        }

    def create(self, validated_data):
        meals_data = validated_data.pop('meals', [])
        macros_planner_id = self.context['macros_planner_id']
        macros_planner = MacrosPlanner.objects.get(id=macros_planner_id)
        diet = Diet.objects.create(macros_planner=macros_planner, **validated_data)

        # Define refeições padrão
        default_meals = [
            {"name": "Breakfast", "time": "07:00:00", "type_of_meal": "Ordinary"},
            {"name": "Lunch", "time": "12:00:00", "type_of_meal": "Ordinary"},
            {"name": "Snack", "time": "15:00:00", "type_of_meal": "Ordinary"},
            {"name": "Dinner", "time": "19:00:00", "type_of_meal": "Ordinary"},
        ]

        context = self.context
        context['diet_id'] = diet.id

        # Adiciona as refeições padrão se não forem fornecidas refeições
        if not meals_data:
            meals_data = default_meals

        for meal_data in meals_data:
            meal_serializer = MealSerializer(data=meal_data, context=context)
            if meal_serializer.is_valid():
                meal_serializer.save()
            else:
                raise serializers.ValidationError(meal_serializer.errors)

        return diet

    def update(self, instance, validated_data):
        meals_data = validated_data.pop('meals', [])
        instance = super().update(instance, validated_data)

        for meal_data in meals_data:
            meal_id = meal_data.get('id')
            if meal_id:
                meal = Meal.objects.get(id=meal_id, diet=instance)
                meal_serializer = MealSerializer(meal, data=meal_data, partial=True, context=self.context)
                if meal_serializer.is_valid():
                    meal_serializer.save()
                else:
                    raise serializers.ValidationError(meal_serializer.errors)
            else:
                meal_serializer = MealSerializer(data=meal_data, context=self.context)
                if meal_serializer.is_valid():
                    meal_serializer.save(diet=instance)
                else:
                    raise serializers.ValidationError(meal_serializer.errors)

        return instance
