from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from apps.macros_sheet.models import MacrosSheet
from apps.macros_sheet.serializers import MacrosSheetSerializer


class MacrosSheetViewSet(viewsets.ModelViewSet):
    queryset = MacrosSheet.objects.all()
    serializer_class = MacrosSheetSerializer
    permission_classes = [IsAuthenticated]

    # Permitir apenas GET e PATCH
    http_method_names = ['get', 'patch']

    def get_queryset(self):
        diet_id = self.kwargs.get('diet_id')
        if diet_id:
            return self.queryset.filter(diet_id=diet_id)
        return super().get_queryset()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        return obj

    def create(self, request, *args, **kwargs):
        # Desativa a criação
        raise MethodNotAllowed(method='POST')

    def destroy(self, request, *args, **kwargs):
        # Desativa a exclusão
        raise MethodNotAllowed(method='DELETE')
