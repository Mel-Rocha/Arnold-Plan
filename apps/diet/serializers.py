from datetime import timedelta
from rest_framework import serializers
from django.core.exceptions import ValidationError

from apps.daily_records.models import DailyRecords
from apps.diet.models import Diet
from apps.macros_sheet.models import MacrosSheet
from apps.meal.models import Meal
from apps.meal.serializers import MealSerializer
from apps.user.models import Nutritionist, Athlete


class DietSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, required=False)
    weeks = serializers.SerializerMethodField()

    class Meta:
        model = Diet
        fields = '__all__'
        extra_kwargs = {
            'nutritionist': {'read_only': True},
            'weeks': {'read_only': True},
        }

    def get_weeks(self, obj):
        if obj.initial_date and obj.final_date:
            delta = obj.final_date - obj.initial_date
            return (delta.days // 7) + 1
        return 1

    def validate(self, data):
        user = self.context['request'].user

        # Verificar se o usuário é um nutricionista
        try:
            nutritionist = Nutritionist.objects.get(user=user)
        except Nutritionist.DoesNotExist:
            raise ValidationError("Only a nutritionist can update the diet.")

        # Verificar se o usuário tem um atleta associado
        athlete = Athlete.objects.filter(nutritionist=nutritionist).first()
        if not athlete:
            raise ValidationError("No athlete associated with this nutritionist.")

        instance = self.instance
        if instance:
            initial_date = data.get('initial_date', instance.initial_date)
            final_date = data.get('final_date', instance.final_date)
        else:
            initial_date = data.get('initial_date')
            final_date = data.get('final_date')

        daily_records = DailyRecords.objects.filter(athlete=athlete)
        if daily_records.exists():
            earliest_record = daily_records.order_by('date').first().date
            latest_record = daily_records.order_by('date').last().date

            if initial_date > earliest_record:
                raise ValidationError(f"Initial date cannot be after the earliest daily record date: {earliest_record}")
            if final_date < latest_record:
                raise ValidationError(f"Final date cannot be before the latest daily record date: {latest_record}")

        return data

    def create(self, validated_data):
        user = self.context['request'].user

        try:
            nutritionist = Nutritionist.objects.get(user=user)
        except Nutritionist.DoesNotExist:
            raise serializers.ValidationError({'nutritionist': 'Nutritionist with the current user does not exist.'})

        diet = Diet.objects.create(nutritionist=nutritionist, **validated_data)

        default_meals = [
            {"name": "Breakfast", "time": "07:00:00", "type_of_meal": "Ordinary", "is_active": True},
            {"name": "Lunch", "time": "12:00:00", "type_of_meal": "Ordinary", "is_active": True},
            {"name": "Snack", "time": "16:00:00", "type_of_meal": "Ordinary", "is_active": True},
            {"name": "Dinner", "time": "19:00:00", "type_of_meal": "Ordinary", "is_active": True}
        ]

        for meal_data in default_meals:
            Meal.objects.create(diet=diet, **meal_data)

        weeks = self.get_weeks(diet)
        for week in range(1, weeks + 1):
            MacrosSheet.objects.create(diet=diet, week=week)

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

        weeks = self.get_weeks(instance)
        current_weeks = instance.macros_sheets.count()

        if weeks > current_weeks:
            for week in range(current_weeks + 1, weeks + 1):
                MacrosSheet.objects.create(diet=instance, week=week)
        elif weeks < current_weeks:
            excess_weeks = instance.macros_sheets.filter(week__gt=weeks)
            for macros_sheet in excess_weeks:
                macros_sheet.delete()

        return instance
