import logging
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.user.models import Athlete
from apps.daily_records.models import DailyRecords


logger = logging.getLogger(__name__)


class DailyRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRecords
        fields = '__all__'
        extra_kwargs = {
            'athlete': {'read_only': True},
            'meal': {'required': True},
            'meal_status': {'required': True},
            'date': {'required': True}
        }

    def validate(self, data):
        meal = data.get('meal')
        date = data.get('date')

        # Verificar se a meal pertence a uma diet cujo intervalo de datas cobre a data do daily_record
        if not (meal.diet.initial_date <= date <= meal.diet.final_date):
            raise ValidationError("The meal's diet does not cover the date of the daily record.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        logger.debug(f"User: {user}")
        athlete = Athlete.objects.get(user=user)
        logger.debug(f"Athlete: {athlete}")

        date = validated_data['date']
        meal = validated_data['meal']
        logger.debug(f"Date: {date}, Meal: {meal}")

        if DailyRecords.objects.filter(athlete=athlete, meal=meal, date=date).exists():
            logger.error("A DailyRecord for this meal and date already exists.")
            raise serializers.ValidationError("A DailyRecord for this meal and date already exists.")

        daily_record_data = validated_data.copy()
        daily_record_data['athlete'] = athlete
        daily_record = DailyRecords.objects.create(**daily_record_data)
        logger.debug(f"Created DailyRecord: {daily_record}")

        return daily_record