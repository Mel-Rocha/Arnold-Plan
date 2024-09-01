from rest_framework import generics
from apps.macros_sheet.models import MealMacrosSheet, DietMacrosSheet
from apps.macros_sheet.serializers import MealMacrosSheetSerializer, DietMacrosSheetSerializer


class MealMacrosSheetDetailView(generics.RetrieveAPIView):
    queryset = MealMacrosSheet.objects.all()
    serializer_class = MealMacrosSheetSerializer


class DietMacrosSheetDetailView(generics.RetrieveAPIView):
    queryset = DietMacrosSheet.objects.all()
    serializer_class = DietMacrosSheetSerializer