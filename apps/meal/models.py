from django.apps import apps
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.models import Core
from apps.diet.models import Diet


class TypeOfMeal(models.TextChoices):
    ORDINARY = 'Ordinary', 'Ordinary'
    FREE_MEAL = 'Free Meal', 'Free Meal'
    PRE_WORKOUT = 'Pre Workout', 'Pre Workout'
    POST_WORKOUT = 'Post Workout', 'Post Workout'


class Meal(Core):
    diet = models.ForeignKey(Diet, related_name='meals', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    time = models.TimeField(default='00:00:00')
    type_of_meal = models.CharField(max_length=50, choices=TypeOfMeal.choices, default=TypeOfMeal.ORDINARY)
    foods = models.JSONField(default=list)

    def __str__(self):
        return f"Meal #{self.id}"


@receiver(post_save, sender=Meal)
def create_meal_macros_sheet(sender, instance, created, **kwargs):
    if created:
        MealMacrosSheet = apps.get_model('macros_sheet', 'MealMacrosSheet')
        MealMacrosSheet.objects.create(meal=instance)
        print(f"MealMacrosSheet created for Meal #{instance.id}")