from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsNutritionistUser
from apps.diet.models import Diet
from apps.diet.serializers import DietSerializer
from config.urls import swagger_safe

class DietViewSet(viewsets.ModelViewSet):
    serializer_class = DietSerializer
    permission_classes = [IsAuthenticated]

    @swagger_safe(Diet)
    def get_queryset(self):
        return Diet.objects.all()

    def perform_create(self, serializer):
        if not IsNutritionistUser().has_permission(self.request, self):
            self.permission_denied(self.request, message="Only nutritionists can create diets.")
        serializer.save()