from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from apps.diet.models import Diet
from apps.user.models import Athlete
from config.urls import swagger_safe
from apps.diet.serializers import DietSerializer
from apps.core.permissions import IsNutritionistUser


class DietViewSet(viewsets.ModelViewSet):
    serializer_class = DietSerializer
    permission_classes = [IsAuthenticated]

    @swagger_safe(Diet)
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'athlete'):
            # Se o usuário é um atleta, filtrar por dietas associadas ao atleta
            return Diet.objects.filter(athlete=user.athlete)
        elif hasattr(user, 'nutritionist'):
            # Se o usuário é um nutricionista, filtrar por dietas dos atletas associados
            return Diet.objects.filter(athlete__nutritionist=user.nutritionist)
        else:
            # Caso contrário, não permitir acesso
            return Diet.objects.none()

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'nutritionist'):
            raise PermissionDenied("Only nutritionists can create diets.")

        # Verificar se o nutricionista está criando uma dieta para um atleta associado a ele
        athlete_id = self.request.data.get('athlete')
        if not athlete_id:
            raise PermissionDenied("Athlete must be specified for the diet.")

        try:
            athlete = Athlete.objects.get(id=athlete_id, nutritionist=self.request.user.nutritionist)
        except Athlete.DoesNotExist:
            raise PermissionDenied("Cannot create a diet for an athlete not associated with this nutritionist.")

        serializer.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user

        if hasattr(user, 'athlete'):
            # Se o usuário é um atleta, não deve ser permitido atualizar a dieta
            raise PermissionDenied("Athletes cannot update diets.")

        if hasattr(user, 'nutritionist'):
            # Se o usuário é um nutricionista, verificar se ele está atualizando a dieta de um atleta associado
            if instance.athlete.nutritionist != user.nutritionist:
                raise PermissionDenied("Cannot update diets for athletes not associated with this nutritionist.")

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if hasattr(user, 'athlete'):
            # Se o usuário é um atleta, não deve ser permitido excluir a dieta
            raise PermissionDenied("Athletes cannot delete diets.")

        if hasattr(user, 'nutritionist'):
            # Se o usuário é um nutricionista, verificar se ele está excluindo a dieta de um atleta associado
            if instance.athlete.nutritionist != user.nutritionist:
                raise PermissionDenied("Cannot delete diets for athletes not associated with this nutritionist.")

        instance.delete()
