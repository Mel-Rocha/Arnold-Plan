from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from apps.macros_sheet.models import MacrosSheet
from apps.macros_sheet.serializers import MacrosSheetSerializer
from apps.diet.models import Diet

class MacrosSheetViewSet(viewsets.ModelViewSet):
    queryset = MacrosSheet.objects.all()
    serializer_class = MacrosSheetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        diet_id = self.kwargs.get('diet_id')
        if diet_id:
            return self.queryset.filter(diet_id=diet_id)
        return super().get_queryset()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        return obj