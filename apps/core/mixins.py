from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin


class AthleteNutritionistPermissionMixin(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin,
                                         UpdateModelMixin, DestroyModelMixin):
    """
    Nutritionist:
    - Permissions: Writing and reading
    - Access: Only to objects associated with him and his athletes.

    Athlete:
    - Permissions: Reading
    - Access: Only to objects associated with the athlete himself.
    """


    def get_queryset(self):
        user = self.request.user
        model_class = self.get_queryset_model_class()

        if hasattr(user, 'athlete'):
            # Se o usuário é um atleta, filtrar por objetos associados ao atleta
            return model_class.objects.filter(athlete=user.athlete)
        elif hasattr(user, 'nutritionist'):
            # Se o usuário é um nutricionista, filtrar por objetos dos atletas associados
            return model_class.objects.filter(athlete__nutritionist=user.nutritionist)
        else:
            # Caso contrário, não permitir acesso
            return model_class.objects.none()


    def get_queryset_model_class(self):
        raise NotImplementedError("Subclasses must implement `get_queryset_model_class`.")


    def perform_create(self, serializer):
        user = self.request.user
        related_model_id = self.get_related_model_id()  # Método para obter o ID do modelo relacionado
        related_model_class = self.get_related_model_class()  # Método para obter a classe do modelo relacionado

        if not related_model_id:
            raise PermissionDenied("Related model must be specified for this operation.")

        try:
            related_model = related_model_class.objects.get(id=related_model_id, nutritionist=user.nutritionist)
        except related_model_class.DoesNotExist:
            raise PermissionDenied("Cannot create object for a related model not associated with this nutritionist.")

        # Salva a instância do serializer com o modelo relacionado corretamente
        serializer.save()


    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user

        if hasattr(user, 'athlete'):
            raise PermissionDenied("Athletes cannot update objects.")

        if hasattr(user, 'nutritionist'):
            if instance.athlete.nutritionist != user.nutritionist:
                raise PermissionDenied("Cannot update objects for athletes not associated with this nutritionist.")

        serializer.save()


    def perform_destroy(self, instance):
        user = self.request.user

        if hasattr(user, 'athlete'):
            raise PermissionDenied("Athletes cannot delete objects.")

        if hasattr(user, 'nutritionist'):
            if instance.athlete.nutritionist != user.nutritionist:
                raise PermissionDenied("Cannot delete objects for athletes not associated with this nutritionist.")

        instance.delete()

    def get_related_model_id(self):
        """
        Método a ser implementado pelas subclasses para obter o ID do modelo relacionado para a operação de criação.
        """
        raise NotImplementedError("Subclasses must implement `get_related_model_id`.")

    def get_related_model_class(self):
        """
        Método a ser implementado pelas subclasses para obter a classe do modelo relacionado para a operação de criação.
        """
        raise NotImplementedError("Subclasses must implement `get_related_model_class`.")

