import datetime

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.diet.models import Diet
from django.contrib.auth import get_user_model
from apps.user.models import Nutritionist, Athlete


User = get_user_model()

@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def create_user():
    """Creates a generic user."""
    def _create_user(username='testuser', password='password', is_nutritionist=False, is_athlete=False):
        user = User.objects.create_user(username=username, password=password)
        user.is_nutritionist = is_nutritionist
        user.is_athlete = is_athlete
        user.save()
        return user
    return _create_user


@pytest.fixture
def create_nutritionist(create_user):
    """Creates a nutritionist from a user."""
    def _create_nutritionist(username='nutritionist', password='password'):
        user = create_user(username=username, password=password, is_nutritionist=True)
        nutritionist = Nutritionist.objects.create(user=user)
        return nutritionist
    return _create_nutritionist


@pytest.fixture
def create_athlete(create_user, create_nutritionist):
    """Creates an athlete linked to a nutritionist."""
    def _create_athlete(username='athlete', password='password', nutritionist=None):
        if nutritionist is None:
            nutritionist = create_nutritionist()  # Se nenhum nutricionista for passado, cria um
        user = create_user(username=username, password=password, is_athlete=True)
        athlete = Athlete.objects.create(
            user=user,
            nutritionist=nutritionist,  # Vincula o atleta ao nutricionista
            birth_date=datetime.date(2000, 1, 1),
            weight=70,
            height=1.70
        )
        return athlete
    return _create_athlete


@pytest.mark.django_db
def test_nutritionist_can_create_diet_for_own_athlete(create_nutritionist, create_athlete):
    # Create a nutritionist
    nutritionist = create_nutritionist(username='nutri')

    # Create an athlete linked to the nutritionist
    athlete = create_athlete(username='athlete', nutritionist=nutritionist)

    # Nutritionist creates a diet for the athlete
    diet = Diet.objects.create(nutritionist=nutritionist, athlete=athlete, name="Cutting Plan")

    assert diet.nutritionist == nutritionist
    assert diet.athlete == athlete


@pytest.mark.django_db
def test_nutritionist_can_create_diet_for_own_athlete(create_nutritionist, create_athlete):
    nutritionist = create_nutritionist(username='nutri')
    athlete = create_athlete(username='athlete', nutritionist=nutritionist)
    diet = Diet.objects.create(
        nutritionist=nutritionist,
        athlete=athlete,
        goal="Cutting Plan",
        observations="Focus on high protein intake",
        initial_date=timezone.now().date(),
        final_date=timezone.now().date() + timezone.timedelta(days=30),
        weeks=4,
        type_of_diet='MAINTENANCE'
    )

    assert diet.nutritionist == nutritionist
    assert diet.athlete == athlete
    assert diet.goal == "Cutting Plan"
    assert diet.observations == "Focus on high protein intake"
    assert diet.weeks == 4
    assert diet.type_of_diet == 'MAINTENANCE'