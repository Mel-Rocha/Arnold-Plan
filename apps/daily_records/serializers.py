import logging
from rest_framework import serializers
from apps.daily_records.models import DailyRecords
from apps.meal.models import Meal
from apps.diet.models import Diet
from apps.user.models import Athlete

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

    def create(self, validated_data):
        # Obtendo o atleta do contexto
        user = self.context['request'].user
        logger.debug(f"User: {user}")
        athlete = Athlete.objects.get(user=user)
        logger.debug(f"Athlete: {athlete}")

        # Verificando se a data está dentro do intervalo de alguma dieta
        date = validated_data['date']
        logger.debug(f"Date: {date}")
        diets = Diet.objects.filter(athlete=athlete, initial_date__lte=date, final_date__gte=date)
        logger.debug(f"Diets: {diets}")

        for diet in diets:
            logger.debug(f"Diet ID: {diet.id}, Initial Date: {diet.initial_date}, Final Date: {diet.final_date}")

        if not diets.exists():
            logger.error("No active diet found for the given date.")
            raise serializers.ValidationError("No active diet found for the given date.")

        # Criando um único registro de refeição
        daily_record_data = validated_data.copy()
        daily_record_data['athlete'] = athlete
        daily_record = DailyRecords.objects.create(**daily_record_data)
        logger.debug(f"Created DailyRecord: {daily_record}")

        return daily_record