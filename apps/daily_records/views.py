from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from apps.user.models import Nutritionist
from apps.core.permissions import IsAthleteUser
from apps.daily_records.models import DailyRecords
from apps.daily_records.serializers import DailyRecordsSerializer
from config.urls import swagger_safe


class DailyRecordsViewSet(viewsets.ModelViewSet):
    serializer_class = DailyRecordsSerializer

    @swagger_safe(DailyRecords)
    def get_queryset(self):
        user = self.request.user

        if user.is_nutritionist:
            try:
                nutritionist = Nutritionist.objects.get(user=user)
                print(f"Nutritionist instance: {nutritionist}")
                return DailyRecords.objects.filter(athlete__nutritionist=nutritionist)
            except Nutritionist.DoesNotExist:
                return DailyRecords.objects.none()
        elif user.is_athlete:
            return DailyRecords.objects.filter(athlete__user=user)
        return DailyRecords.objects.none()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAthleteUser()]
