from drf_yasg import openapi
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from apps.user.models import Nutritionist
from apps.core.decorators import swagger_safe
from apps.core.permissions import IsAthleteUser
from apps.daily_records.models import DailyRecords
from apps.daily_records.serializers import DailyRecordsSerializer


class DailyRecordsViewSet(viewsets.ModelViewSet):
    serializer_class = DailyRecordsSerializer

    @swagger_safe(DailyRecords)
    def get_queryset(self):
        user = self.request.user

        if user.is_nutritionist:
            try:
                nutritionist = Nutritionist.objects.get(user=user)
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date of the range (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date of the range (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: DailyRecordsSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='by-date')
    def get_by_date(self, request):
        """
        Objective: Get all daily records of all meals on the specific day

        params:
        date: str

        return: list
        """
        date = request.query_params.get('date')
        if not date:
            return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset().filter(date=date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date of the range (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date of the range (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: DailyRecordsSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='by-date-range')
    def get_by_date_range(self, request):
        """
        Objective: Get all daily records of all meals in the date range.

        params:
        start_date: str
        end_date: str

        return: list
        """
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not start_date or not end_date:
            return Response({"error": "Start date and end date parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset().filter(date__range=[start_date, end_date])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'diet_id', openapi.IN_QUERY,
                description="ID of the diet to filter records",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: DailyRecordsSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='by-diet')
    def get_by_diet(self, request):
        """
        Objective: Get all daily records of all meals from all days of a specific diet.

        params:
        diet_id: int

        return: list
        """
        diet_id = request.query_params.get('diet_id')
        if not diet_id:
            return Response({"error": "Diet ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset().filter(meal__diet_id=diet_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
