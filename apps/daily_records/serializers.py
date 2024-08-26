from rest_framework import serializers

from apps.user.models import Athlete
from apps.daily_records.models import DailyRecords


class DailyRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRecords
        fields = '__all__'
        extra_kwargs = {
            'athlete': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context['request']
        athlete = Athlete.objects.get(user=request.user)
        validated_data['athlete'] = athlete
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('athlete', None)
        return super().update(instance, validated_data)
