from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsNutritionistUser(BasePermission):
    """
    Allows access to Nutritionist users
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_nutritionist

class IsAthleteUser(BasePermission):
    """
    Allows access to Athlete users
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_athlete


class IsNotAthleteUserAndIsNotNutritionist(BasePermission):
    """
    Allows access to users who are neither athletes nor users
    """
    def has_permission(self, request, view):
        return not (request.user.is_athlete or request.user.is_nutritionist)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        SAFE_METHODS are allowed for any request,
        but write permissions are only allowed to the owner of the object.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
