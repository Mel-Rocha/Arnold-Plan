from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from apps.core.mixins import AthleteNutritionistPermissionMixin
from apps.diet.models import Diet
from apps.user.models import Athlete
from config.urls import swagger_safe
from apps.diet.serializers import DietSerializer
from apps.core.permissions import IsNutritionistUser


class DietViewSet(AthleteNutritionistPermissionMixin):
    serializer_class = DietSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset_model_class(self):
        return Diet
