from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from apps.macros_sheet.models import MacrosSheet
from apps.macros_sheet.serializers import MacrosSheetSerializer
from apps.diet.models import Diet

class MacrosSheetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, diet_id, format=None):
        diet = get_object_or_404(Diet, id=diet_id)
        macros_sheets = MacrosSheet.objects.filter(diet=diet)
        serializer = MacrosSheetSerializer(macros_sheets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MacrosSheetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, diet_id, macros_sheet_id, format=None):
        macros_sheet = get_object_or_404(MacrosSheet, id=macros_sheet_id, diet_id=diet_id)
        serializer = MacrosSheetSerializer(macros_sheet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, diet_id, macros_sheet_id, format=None):
        macros_sheet = get_object_or_404(MacrosSheet, id=macros_sheet_id, diet_id=diet_id)
        serializer = MacrosSheetSerializer(macros_sheet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


