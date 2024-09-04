from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound

from apps.core.permissions import IsNutritionistUser, IsAthleteUser
from apps.macros_sheet.models import MealMacrosSheet, DietMacrosSheet
from apps.macros_sheet.serializers import MealMacrosSheetSerializer, DietMacrosSheetSerializer


class MealMacrosSheetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        user = self.request.user
        if user.is_athlete:
            self.permission_classes = [IsAuthenticated, IsAthleteUser]
        elif user.is_nutritionist:
            self.permission_classes = [IsAuthenticated, IsNutritionistUser]
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='all')
    def list_all(self, request):
        user = request.user
        if user.is_athlete:
            queryset = MealMacrosSheet.objects.filter(meal__diet__athlete=user.athlete)
        elif user.is_nutritionist:
            queryset = MealMacrosSheet.objects.filter(meal__diet__athlete__nutritionist=user.nutritionist)
        else:
            raise PermissionDenied("Você não tem permissão para acessar este recurso.")
        serializer = MealMacrosSheetSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='athlete/(?P<athlete_id>[^/.]+)')
    def list_by_athlete(self, request, athlete_id=None):
        user = request.user
        if not user.is_nutritionist:
            raise PermissionDenied("Você não tem permissão para acessar este recurso.")
        queryset = MealMacrosSheet.objects.filter(meal__diet__athlete__id=athlete_id, meal__diet__athlete__nutritionist=user.nutritionist)
        serializer = MealMacrosSheetSerializer(queryset, many=True)
        return Response(serializer.data)


class DietMacrosSheetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        user = self.request.user
        if user.is_athlete:
            self.permission_classes = [IsAuthenticated, IsAthleteUser]
        elif user.is_nutritionist:
            self.permission_classes = [IsAuthenticated, IsNutritionistUser]
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='all')
    def list_all(self, request):
        user = request.user
        if user.is_athlete:
            queryset = DietMacrosSheet.objects.filter(diet__athlete=user.athlete)
        elif user.is_nutritionist:
            queryset = DietMacrosSheet.objects.filter(diet__athlete__nutritionist=user.nutritionist)
        else:
            raise PermissionDenied("Você não tem permissão para acessar este recurso.")
        serializer = DietMacrosSheetSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='athlete/(?P<athlete_id>[^/.]+)')
    def list_by_athlete(self, request, athlete_id=None):
        user = request.user
        if not user.is_nutritionist:
            raise PermissionDenied("Você não tem permissão para acessar este recurso.")
        queryset = DietMacrosSheet.objects.filter(diet__athlete__id=athlete_id, diet__athlete__nutritionist=user.nutritionist)
        serializer = DietMacrosSheetSerializer(queryset, many=True)
        return Response(serializer.data)