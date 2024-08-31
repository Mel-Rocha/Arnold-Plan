from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.diet.models import Diet
from config.urls import swagger_safe
from apps.diet.serializers import DietSerializer
from apps.core.permissions import IsNutritionistUser


class DietViewSet(viewsets.ModelViewSet):
    serializer_class = DietSerializer
    permission_classes = [IsAuthenticated]

    @swagger_safe(Diet)
    def get_queryset(self):
        queryset = Diet.objects.select_related('nutritionist').prefetch_related('meals').all()
        return queryset

    def perform_create(self, serializer):
        if not IsNutritionistUser().has_permission(self.request, self):
            self.permission_denied(self.request, message="Only nutritionists can create diets.")
        serializer.save()
