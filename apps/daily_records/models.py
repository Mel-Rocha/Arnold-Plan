from django.db import models
from django.core.exceptions import ValidationError

from apps.core.models import Core
from apps.meal.models import Meal
from apps.user.models import Athlete
from apps.core.validators import validate_not_in_future


class MealStatus(models.TextChoices):
    DONE = 'done', 'Done'
    PARTIALLY_DONE = 'partially_done', 'Partially Done'
    NOT_DONE = 'not_done', 'Not Done'


class FeelingStatus(models.TextChoices):
    HAPPY = 'happy', 'Happy'
    QUIET = 'quiet', 'Quiet'
    NORMAL = 'normal', 'Normal'
    SAD = 'sad', 'Sad'
    ANGER = 'anger', 'Anger'
    ANXIETY = 'anxiety', 'Anxiety'
    FEAR = 'fear', 'Fear'


class AppetiteStatus(models.TextChoices):
    HUNGER = 'hunger', 'Hunger'
    DESIRE_TO_EAT = 'desire_to_eat', 'Desire to Eat'
    SATISFIED = 'satisfied', 'Satisfied'
    STEW = 'stew', 'Stew'


class DailyRecords(Core):
    athlete = models.ForeignKey(Athlete, related_name='Athlete', on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, related_name='daily_records', on_delete=models.PROTECT)
    date = models.DateField(validators=[validate_not_in_future])

    meal_status = models.CharField(
        max_length=20,
        choices=MealStatus.choices,
    )
    feeling_status = models.CharField(
        max_length=10,
        choices=FeelingStatus.choices,
        blank=True,
    )
    appetite_status = models.CharField(
        max_length=15,
        choices=AppetiteStatus.choices,
        blank=True,
    )
    food_replacement = models.TextField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Validation to ensure that food_replacement is mandatory in cases of "Partially Done" or "Not Done"
        if self.meal_status in [MealStatus.PARTIALLY_DONE, MealStatus.NOT_DONE] and not self.food_replacement:
            raise ValidationError("Food replacement is required for 'Partially Done' or 'Not Done' status.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Daily Record #{self.id} for {self.athlete} on {self.date}"


