import logging

from rest_framework import serializers

from apps.meal.models import Meal
from apps.diet.models import Diet
from apps.taco.utils import get_retention_db_connection


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MealSerializer(serializers.ModelSerializer):
    foods = serializers.ListField()

    class Meta:
        model = Meal
        fields = '__all__'
        extra_kwargs = {
            'diet': {'read_only': True},  # Diet ID is read-only and will be set automatically
            'is_active': {'default': True}  # Default value for is_active
        }

    def create(self, validated_data):
        foods = validated_data.pop('foods', [])
        diet_id = self.context['diet_id']
        diet = Diet.objects.get(id=diet_id)

        validated_data.pop('diet', None)
        meal = Meal.objects.create(diet=diet, **validated_data)

        for food in foods:
            food_id = food.get('food_id')
            quantity = food.get('quantity')

            if not (1 <= food_id <= 597):
                raise serializers.ValidationError("Food ID must be between 1 and 597.")

            # Fetch complete food details in the holding bank and adjust values
            food_details = self.get_food_details(food_id, quantity)

            # Add full food details to the meal's food list
            meal.foods.append(food_details)

        meal.save()
        return meal

    def update(self, instance, validated_data):
        foods = validated_data.pop('foods', [])
        instance = super().update(instance, validated_data)

        instance.foods.clear()  # Clear existing list of foods before updating

        for food in foods:
            food_id = food.get('food_id')
            quantity = food.get('quantity')

            if not (1 <= food_id <= 597):
                raise serializers.ValidationError("Food ID must be between 1 and 597.")

            # Fetch complete food details in the holding bank and adjust values
            food_details = self.get_food_details(food_id, quantity)

            # Add full food details to the meal's food list
            instance.foods.append(food_details)

        instance.save()
        return instance

    def get_food_details(self, food_id, amount):
        # Implementation to fetch food details from the retention bank and adjust values
        query = "SELECT * FROM CMVColtaco3 WHERE id = %s"
        params = [food_id]

        with get_retention_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()

                if row:
                    columns = [col[0] for col in cursor.description]
                    food = dict(zip(columns, row))

                    # Ajustar os valores com base no 'amount'
                    for key in food:
                        if key not in ['id', 'food_description', 'category']:
                            try:
                                value = float(food[key])
                                food[key] = round((value * amount) / 100, 3)
                            except ValueError:
                                # If the conversion to float fails, it keeps the original value
                                continue

                    # Add quantity to food details dictionary
                    food['quantity'] = amount

                    return food
                else:
                    raise serializers.ValidationError(f"Alimento com ID {food_id} não encontrado.")
