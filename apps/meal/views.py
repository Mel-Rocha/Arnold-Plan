from rest_framework import viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from apps.core.permissions import IsNutritionistUser, IsAthleteUser
from apps.meal.models import Meal
from apps.diet.models import Diet
from config.urls import swagger_safe
from apps.meal.serializers import MealSerializer


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        user = self.request.user
        if user.is_athlete:
            self.permission_classes = [IsAuthenticated, IsAthleteUser]
        elif user.is_nutritionist:
            self.permission_classes = [IsAuthenticated, IsNutritionistUser]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        diet_id = self.kwargs.get('diet_id')

        try:
            diet = Diet.objects.get(id=diet_id)
        except Diet.DoesNotExist:
            raise NotFound(f'Diet with id {diet_id} does not exist')

        if user.is_athlete:
            if diet.athlete != user.athlete:
                raise PermissionDenied("You can only access meals for your own diet.")
            return Meal.objects.filter(diet=diet)
        elif user.is_nutritionist:
            if diet.athlete.nutritionist != user.nutritionist:
                raise PermissionDenied("You cannot access meals for diets not associated with your athletes.")
            return Meal.objects.filter(diet=diet)
        else:
            return Meal.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        diet_id = self.kwargs.get('diet_id')

        try:
            diet = Diet.objects.get(id=diet_id)
        except Diet.DoesNotExist:
            raise NotFound(f'Diet with id {diet_id} does not exist')

        if user.is_athlete:
            raise PermissionDenied("You cannot create meals.")

        if user.is_nutritionist:
            if diet.athlete.nutritionist != user.nutritionist:
                raise PermissionDenied("You cannot create meals for diets not associated with your athletes.")

        # Adiciona o `diet_id` ao contexto do serializer
        serializer.context['diet_id'] = diet_id
        serializer.save(diet=diet)

    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user

        if user.is_athlete:
            raise PermissionDenied("You cannot update meals.")

        if user.is_nutritionist:
            if instance.diet.athlete.nutritionist != user.nutritionist:
                raise PermissionDenied("You cannot update meals for diets not associated with your athletes.")

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if user.is_athlete:
            raise PermissionDenied("You cannot delete meals.")

        if user.is_nutritionist:
            if instance.diet.athlete.nutritionist != user.nutritionist:
                raise PermissionDenied("You cannot delete meals for diets not associated with your athletes.")

        instance.delete()
