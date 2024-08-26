from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.user.views import (MyTokenObtainPairView, UpdatePasswordView, AthleteViewSet, NutritionistViewSet,
                             UserCreateView)

router = DefaultRouter()
router.register(r'athlete', AthleteViewSet, basename='athlete')
router.register(r'nutritionist', NutritionistViewSet, basename='nutritionist')

token_and_passwords_user = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('password/update/', UpdatePasswordView.as_view(), name='password_update'),
    path('user/create/', UserCreateView.as_view({'post': 'create'}), name='user_create'),
]


urlpatterns = [
    path('', include(router.urls)),
] + token_and_passwords_user