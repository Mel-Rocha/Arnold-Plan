import datetime

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.meal.models import Meal
from apps.diet.models import Diet
from apps.user.models import User
from django.contrib.auth import get_user_model
from apps.daily_records.models import DailyRecords
from apps.user.models import Athlete, Nutritionist


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
            nutritionist = create_nutritionist()
        user = create_user(username=username, password=password, is_athlete=True)
        athlete = Athlete.objects.create(
            user=user,
            nutritionist=nutritionist,
            birth_date=datetime.date(2000, 1, 1),
            weight=70,
            height=1.70
        )
        return athlete
    return _create_athlete

@pytest.fixture
def create_diet(create_nutritionist, create_athlete):
    """Cria uma dieta vinculada a um atleta e a um nutricionista."""
    def _create_diet(athlete=None):
        if athlete is None:
            athlete = create_athlete()

        diet = Diet.objects.create(
            athlete=athlete,
            nutritionist=athlete.nutritionist,
            goal="Cutting Plan",
            observations="Focus on high protein intake",
            initial_date="2024-09-05",
            final_date="2024-10-05",
            weeks=4,
            type_of_diet='MAINTENANCE'
        )

        Meal.objects.create(diet=diet, name="Breakfast", time="08:00:00")
        Meal.objects.create(diet=diet, name="Lunch", time="12:00:00")
        Meal.objects.create(diet=diet, name="Dinner", time="19:00:00")

        return diet

    return _create_diet


@pytest.fixture
def create_daily_record(create_athlete, create_diet):
    def _create_daily_record(athlete=None, meal=None, diet=None, date=None, meal_status='Done',
                             feeling_status='Good', appetite_status='Normal',
                             food_replacement='N/A', observations=''):
        if athlete is None:
            athlete = create_athlete()
        if date is None:
            date = timezone.now().date()
        if diet is None:
            diet = create_diet(athlete=athlete)

        if meal is None:
            meal = diet.meals.first()

        daily_record = DailyRecords.objects.create(
            athlete=athlete,
            meal=meal,
            date=date,
            meal_status=meal_status,
            feeling_status=feeling_status,
            appetite_status=appetite_status,
            food_replacement=food_replacement,
            observations=observations
        )
        return daily_record

    return _create_daily_record


@pytest.mark.django_db
def test_daily_record_creation(create_daily_record, create_athlete, create_diet):
    athlete = create_athlete(username='athlete')

    diet = create_diet(athlete=athlete)

    daily_record = create_daily_record(
        athlete=athlete,
        diet=diet,
        date='2024-09-05',
        meal_status='Done',
        feeling_status='Good',
        appetite_status='Normal',
        food_replacement='N/A',
        observations='All good.'
    )

    assert daily_record.athlete == athlete
    assert daily_record.meal in diet.meals.all()
    assert daily_record.date == '2024-09-05'
    assert daily_record.meal_status == 'Done'
    assert daily_record.feeling_status == 'Good'
    assert daily_record.appetite_status == 'Normal'
    assert daily_record.food_replacement == 'N/A'
    assert daily_record.observations == 'All good.'


@pytest.mark.django_db
def test_daily_record_duplicate_failure(api_client, create_daily_record, create_athlete, create_diet):
    athlete = create_athlete(username='athlete')
    diet = create_diet(athlete=athlete)

    api_client.force_authenticate(user=athlete.user)

    response = api_client.post(reverse('daily_records-list'), {
        'athlete': athlete.id,
        'meal': diet.meals.first().id,
        'date': '2024-09-05',
        "meal_status": "done",
        "feeling_status": "happy",
        "appetite_status": "hunger",
        'food_replacement': 'N/A',
        'observations': 'All good.'
    })

    print(f'First response status: {response.status_code}')
    print(f'First response data: {response.data}')

    assert response.status_code == status.HTTP_201_CREATED

    response = api_client.post(reverse('daily_records-list'), {
        'athlete': athlete.id,
        'meal': diet.meals.first().id,
        'date': '2024-09-05',  # Some day
        "meal_status": "done",
        "feeling_status": "happy",
        "appetite_status": "hunger",
        'food_replacement': 'N/A',
        'observations': 'Should fail due to duplicate.'
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert 'A DailyRecord for this meal and date already exists.' in response.data