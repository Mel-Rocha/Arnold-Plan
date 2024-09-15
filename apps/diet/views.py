from rest_framework import status
from openpyxl import Workbook
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.diet.models import Diet
from apps.user.models import Athlete
from apps.core.permissions import IsAthleteUser
from apps.diet.serializers import DietSerializer
from apps.daily_records.models import DailyRecords
from apps.core.mixins import AthleteNutritionistPermissionMixin


class DietViewSet(AthleteNutritionistPermissionMixin):
    serializer_class = DietSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset_model_class(self):
        return Diet

    def get_related_model_id(self):
        return self.request.data.get('athlete')

    def get_related_model_class(self):
        return Athlete

    @action(detail=False, methods=['get'], url_path='diet-count', permission_classes=[IsAuthenticated, IsAthleteUser])
    def diet_dates(self, request):
        diets = Diet.objects.all().values('id', 'initial_date', 'final_date')
        return Response(diets)


    def destroy(self, request, *args, **kwargs):
        diet = self.get_object()
        daily_records = DailyRecords.objects.filter(meal__diet=diet)

        if daily_records.exists():
            return Response(
                {"detail": "Cannot delete this diet because the athlete has already started executing it and has daily records associated with its meals."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get'], url_path='export', permission_classes=[IsAuthenticated])
    def export_diet(self, request, pk=None):
        diet = self.get_object()
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=diet_{diet.id}.xlsx'

        wb = Workbook()
        ws = wb.active
        ws.title = "Diet"

        # Add headers
        headers = ["Meal Name", "Time", "Type of Meal", "Food Name", "Quantity", "Unit"]
        ws.append(headers)

        # Add meal and food data
        for meal in diet.meals.all():
            for food in meal.foods:
                ws.append([
                    meal.name,
                    meal.time,
                    meal.type_of_meal,
                    food['energy_kcal'],
                    food['protein'],
                    food['carbohydrates'],
                    food['lipids'],
                    food['quantity'],
                    food['dietary_fiber'],
                    food['food_description']
                ])

        wb.save(response)
        return response