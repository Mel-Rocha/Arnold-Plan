from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from apps.user.models import Nutritionist
from apps.macros_planner.models import MacrosPlanner
from apps.core.permissions import IsNutritionistUser
from apps.macros_planner.serializers import MacrosPlannerSerializer
from config.urls import swagger_safe


class MacrosPlannerViewSet(viewsets.ModelViewSet):
    serializer_class = MacrosPlannerSerializer


    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsNutritionistUser()]

    @swagger_safe(MacrosPlanner)
    def get_queryset(self):

        user = self.request.user

        if user.is_nutritionist:
            return MacrosPlanner.objects.filter(nutritionist__user=user)
        elif user.is_athlete:
            return MacrosPlanner.objects.filter(athlete__user=user)
        else:
            return MacrosPlanner.objects.none()


    def list(self, request, *args, **kwargs):

        user = request.user

        if user.is_nutritionist:
            queryset = MacrosPlanner.objects.filter(nutritionist__user=user)
        elif user.is_athlete:
            queryset = MacrosPlanner.objects.filter(athlete__user=user)
        else:
            queryset = MacrosPlanner.objects.none()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        user = self.request.user

        if user.is_nutritionist:
            if instance.nutritionist.user != user:
                raise PermissionDenied("Você não tem permissão para acessar este MacrosPlanner.")
        elif user.is_athlete:
            if instance.athlete.user != user:
                raise PermissionDenied("Você não tem permissão para acessar este MacrosPlanner.")
        else:
            raise PermissionDenied("Você não tem permissão para acessar este MacrosPlanner.")

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        if user.is_nutritionist:
            athlete_id = serializer.validated_data['athlete'].id
            if not Nutritionist.objects.filter(user=user, athletes__id=athlete_id).exists():
                raise PermissionDenied("Você não tem permissão para criar um MacrosPlanner para este atleta.")
        elif user.is_athlete:
            raise PermissionDenied("Você não tem permissão para criar um MacrosPlanner.")

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user = request.user

        if user.is_nutritionist:
            if instance.nutritionist.user != user:
                raise PermissionDenied("Você não tem permissão para atualizar este MacrosPlanner.")
        elif user.is_athlete:
            raise PermissionDenied("Você não tem permissão para atualizar um MacrosPlanner.")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        user = request.user

        if user.is_nutritionist:
            if instance.nutritionist.user != user:
                raise PermissionDenied("Você não tem permissão para excluir este MacrosPlanner.")
        elif user.is_athlete:
            raise PermissionDenied("Você não tem permissão para excluir um MacrosPlanner.")

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
