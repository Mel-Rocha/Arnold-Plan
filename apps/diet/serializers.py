from rest_framework import serializers

from apps.macros_sheet.models import MacrosSheet
from apps.meal.models import Meal
from apps.diet.models import Diet
from apps.user.models import Nutritionist
from apps.meal.serializers import MealSerializer


class DietSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, required=False)

    class Meta:
        model = Diet
        fields = '__all__'
        extra_kwargs = {
            'nutritionist': {'read_only': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user

        try:
            nutritionist = Nutritionist.objects.get(user=user)
        except Nutritionist.DoesNotExist:
            raise serializers.ValidationError({'nutritionist': 'Nutritionist with the current user does not exist.'})

        # Criação da Diet
        diet = Diet.objects.create(nutritionist=nutritionist, **validated_data)

        # Definindo as refeições padrão
        default_meals = [
            {"name": "Breakfast", "time": "07:00:00", "type_of_meal": "Ordinary", "is_active": True},
            {"name": "Lunch", "time": "12:00:00", "type_of_meal": "Ordinary", "is_active": True},
            {"name": "Snack", "time": "16:00:00", "type_of_meal": "Ordinary", "is_active": True},
            {"name": "Dinner", "time": "19:00:00", "type_of_meal": "Ordinary", "is_active": True}
        ]

        # Criando as refeições padrão
        for meal_data in default_meals:
            Meal.objects.create(diet=diet, **meal_data)

        # Criação das MacrosSheets baseadas nas semanas
        weeks = validated_data.get('weeks', 0)
        for week in range(1, weeks + 1):
            MacrosSheet.objects.create(diet=diet, week=week)

        return diet

    def update(self, instance, validated_data):
        meals_data = validated_data.pop('meals', [])
        instance = super().update(instance, validated_data)

        # Atualizando ou criando refeições
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

        # Atualizando o número de MacrosSheets
        weeks = validated_data.get('weeks', 0)
        current_weeks = instance.macros_sheets.count()

        if weeks > current_weeks:
            for week in range(current_weeks + 1, weeks + 1):
                MacrosSheet.objects.create(diet=instance, week=week)
        elif weeks < current_weeks:
            # Remover semanas extras, se necessário
            excess_weeks = instance.macros_sheets.filter(week__gt=weeks)
            for macros_sheet in excess_weeks:
                macros_sheet.delete()

        return instance