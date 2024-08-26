from rest_framework import serializers

from apps.meal.models import Meal
from apps.diet.models import Diet
from apps.food_options.models import FoodOptions
from apps.food_options.serializers import FoodOptionsSerializer


class MealSerializer(serializers.ModelSerializer):
    food_options = FoodOptionsSerializer(many=True, required=False)

    class Meta:
        model = Meal
        fields = '__all__'
        extra_kwargs = {
            'diet': {'read_only': True}  # Diet ID is read-only and will be set automatically
        }

    def create(self, validated_data):
        food_options_data = validated_data.pop('food_options', [])
        diet_id = self.context['diet_id']
        diet = Diet.objects.get(id=diet_id)

        validated_data.pop('diet', None)

        meal = Meal.objects.create(diet=diet, **validated_data)

        for food_option_data in food_options_data:
            FoodOptions.objects.create(meal=meal, **food_option_data)

        return meal

    def update(self, instance, validated_data):
        food_options_data = validated_data.pop('food_options', [])
        instance = super().update(instance, validated_data)

        for food_option_data in food_options_data:
            food_option_id = food_option_data.get('id')
            if food_option_id:
                food_option = FoodOptions.objects.get(id=food_option_id, meal=instance)
                for key, value in food_option_data.items():
                    setattr(food_option, key, value)
                food_option.save()
            else:
                FoodOptions.objects.create(meal=instance, **food_option_data)

        return instance
