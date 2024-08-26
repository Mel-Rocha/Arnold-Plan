from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from apps.core.permissions import IsNutritionistUser
from apps.macros_sheet.models import MacrosSheet
from apps.macros_sheet.serializers import MacrosSheetSerializer
from config.urls import swagger_safe


class MacrosSheetViewSet(viewsets.ModelViewSet):
    serializer_class = MacrosSheetSerializer

    @swagger_safe(MacrosSheet)
    def get_queryset(self):
        macros_planner_id = self.kwargs.get('macros_planner_id')
        return MacrosSheet.objects.filter(macros_planner_id=macros_planner_id)

    def perform_create(self, serializer):
        macros_planner_id = self.kwargs.get('macros_planner_id')
        serializer.context['macros_planner_id'] = macros_planner_id
        serializer.save()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsNutritionistUser()]
