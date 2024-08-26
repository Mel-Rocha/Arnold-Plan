from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from apps.core import gateway
from apps.core.gateway import response_log_user
from apps.user.models import  Nutritionist, Athlete
from apps.core.permissions import IsNotAthleteUserAndIsNotNutritionist, IsOwnerOrReadOnly
from apps.user.serializers import MyTokenObtainPairSerializer, UpdatePasswordSerializer, \
    UserSerializerCreateOrUpdate, AthleteSerializer, NutritionistSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateView(gateway.Create):
    permission_classes = []
    serializer_class = UserSerializerCreateOrUpdate

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'is_active': user.is_active,
                'is_nutritionist': user.is_nutritionist,
                'is_athlete': user.is_athlete,
            }
            return response_log_user(request, user_data, 201)
        except IntegrityError:
            return response_log_user(request, "Integrity error.", 409)
        except Exception as e:
            return response_log_user(request, str(e), 400)


# Athlete
class AthleteViewSet(viewsets.ModelViewSet):
    """
    Mandatory to provide:
    - provide in header
    @access_token: string (Bearer Token)
    """
    queryset = Athlete.objects.filter(user__is_active=True)
    serializer_class = AthleteSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsAuthenticated(), IsNotAthleteUserAndIsNotNutritionist()]
        return [IsAuthenticated(), IsOwnerOrReadOnly()]


# Nutritionist
class NutritionistViewSet(viewsets.ModelViewSet):
    """
    Mandatory to provide:
    - provide in header
    @access_token: string (Bearer Token)
    """
    queryset = Nutritionist.objects.filter(user__is_active=True)
    serializer_class = NutritionistSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsAuthenticated(), IsNotAthleteUserAndIsNotNutritionist()]
        return [IsAuthenticated(), IsOwnerOrReadOnly()]
