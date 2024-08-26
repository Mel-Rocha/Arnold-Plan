from django.db import models

from apps.core.models import Core
from apps.diet.models import Diet


class TypeOfMeal(models.TextChoices):
    ORDINARY = 'Ordinary', 'Ordinary'
    FREE_MEAL = 'Free Meal', 'Free Meal'
    PRE_WORKOUT = 'Pre Workout', 'Pre Workout'
    POST_WORKOUT = 'Post Workout', 'Post Workout'


class Meal(Core):
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    time = models.TimeField(default='00:00:00')
    type_of_meal = models.CharField(max_length=50, choices=TypeOfMeal.choices, default=TypeOfMeal.ORDINARY)

    def __str__(self):
        return f"Meal #{self.id}"
