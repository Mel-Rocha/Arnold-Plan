from rest_framework import generics
from apps.macros_sheet.models import MealMacrosSheet
from apps.macros_sheet.serializers import MealMacrosSheetSerializer

class MealMacrosSheetDetailView(generics.RetrieveAPIView):
    queryset = MealMacrosSheet.objects.all()
    serializer_class = MealMacrosSheetSerializer
