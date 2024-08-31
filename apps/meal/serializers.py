from rest_framework import serializers
from apps.meal.models import Meal
from apps.diet.models import Diet
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MealSerializer(serializers.ModelSerializer):
    foods = serializers.JSONField()

    class Meta:
        model = Meal
        fields = '__all__'
        extra_kwargs = {
            'diet': {'read_only': True},  # Diet ID is read-only and will be set automatically
            'is_active': {'default': True}  # Default value for is_active
        }

    def create(self, validated_data):
        foods = validated_data.pop('foods', [])
        if not isinstance(foods, list):
            raise serializers.ValidationError("Foods must be a list of dictionaries.")

        diet_id = self.context['diet_id']
        diet = Diet.objects.get(id=diet_id)

        validated_data.pop('diet', None)
        meal = Meal.objects.create(diet=diet, **validated_data)

        for food in foods:
            if not isinstance(food, dict):
                raise serializers.ValidationError("Each food entry must be a dictionary.")

            food_id = food.get('food_id')
            quantity = food.get('quantity')

            if not (1 <= food_id <= 597):
                raise serializers.ValidationError("Food ID must be between 1 and 597.")

            logger.debug(f'Adding food with ID: {food_id} and quantity: {quantity}')
            meal.foods.append({
                'food_id': food_id,
                'quantity': quantity
            })

        meal.save()
        return meal

    def update(self, instance, validated_data):
        foods = validated_data.pop('foods', [])
        if not isinstance(foods, list):
            raise serializers.ValidationError("Foods must be a list of dictionaries.")

        instance = super().update(instance, validated_data)

        for food in foods:
            if not isinstance(food, dict):
                raise serializers.ValidationError("Each food entry must be a dictionary.")

            food_id = food.get('food_id')
            quantity = food.get('quantity')

            if not (1 <= food_id <= 597):
                raise serializers.ValidationError("Food ID must be between 1 and 597.")

            logger.debug(f'Adding food with ID: {food_id} and quantity: {quantity}')
            instance.foods.append({
                'food_id': food_id,
                'quantity': quantity
            })

        instance.save()
        return instance
