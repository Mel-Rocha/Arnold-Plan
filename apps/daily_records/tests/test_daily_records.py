import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from apps.daily_records.models import DailyRecords
from apps.user.models import Nutritionist, Athlete
from apps.meal.models import  Meal
from apps.diet.models import Diet
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
@pytest.mark.django_db
def create_user():
    def _create_user(username='testuser', password='password'):
        user = User.objects.create_user(username=username, password=password)
        return user
    return _create_user

@pytest.fixture
def create_nutritionist(create_user):
    user = create_user(username='nutritionist', password='password')
    Nutritionist.objects.create(user=user)
    return user

@pytest.fixture
def create_athlete(create_user):
    user = create_user(username='athlete', password='password')
    Athlete.objects.create(user=user)
    return user

@pytest.fixture
def create_diet(create_nutritionist, create_athlete):
    nutritionist = create_nutritionist
    athlete = create_athlete
    diet = Diet.objects.create(name="Test Diet", nutritionist=nutritionist)
    Meal.objects.create(name="Breakfast", diet=diet)
    Meal.objects.create(name="Lunch", diet=diet)
    return diet, athlete

@pytest.fixture
@pytest.mark.django_db
def create_records(create_diet):
    diet, athlete = create_diet
    date_today = timezone.now().date()
    DailyRecords.objects.create(
        athlete=athlete,
        meal=Meal.objects.first(),
        date=date_today
    )
    DailyRecords.objects.create(
        athlete=athlete,
        meal=Meal.objects.last(),
        date=date_today
    )

def test_get_daily_records_by_date(api_client, create_records, create_athlete):
    user = create_athlete
    api_client.force_authenticate(user=user)
    date_today = timezone.now().date()
    url = reverse('dailyrecords-by-date') + f'?date={date_today}'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2  # Assuming 2 records are created

def test_get_daily_records_by_date_range(api_client, create_records, create_athlete):
    user = create_athlete
    api_client.force_authenticate(user=user)
    start_date = (timezone.now() - timezone.timedelta(days=1)).date()
    end_date = timezone.now().date()
    url = reverse('dailyrecords-by-date-range') + f'?start_date={start_date}&end_date={end_date}'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2  # Assuming 2 records are created

def test_get_daily_records_by_diet(api_client, create_records, create_nutritionist):
    user = create_nutritionist
    api_client.force_authenticate(user=user)
    diet_id = Diet.objects.first().id
    url = reverse('dailyrecords-by-diet') + f'?diet_id={diet_id}'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2  # Assuming 2 records are created

def test_get_daily_records_permissions(api_client, create_athlete):
    url = reverse('dailyrecords-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    user = create_athlete
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
