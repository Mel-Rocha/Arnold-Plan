from rest_framework import viewsets

from apps.diet.models import Diet
from apps.diet.serializers import DietSerializer
from config.urls import swagger_safe


class DietViewSet(viewsets.ModelViewSet):
    serializer_class = DietSerializer

    @swagger_safe(Diet)
    def get_queryset(self):
        return Diet.objects.filter(macros_planner=self.kwargs['macros_planner_id'])

    def perform_create(self, serializer):
        serializer.context['macros_planner_id'] = self.kwargs['macros_planner_id']
        serializer.save()
