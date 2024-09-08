from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.diet.models import Diet
from apps.user.models import Athlete
from apps.diet.serializers import DietSerializer
from apps.core.permissions import IsAthleteUser
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
