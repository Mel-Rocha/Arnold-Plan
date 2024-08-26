from django.db import models

from apps.core.models import Core
from apps.user.models import Athlete


class DailyRecords(Core):
    TIME_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]

    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, default=None)

    date = models.DateField()

    morning_meal = models.BooleanField(default=False)
    afternoon_meal = models.BooleanField(default=False)
    evening_meal = models.BooleanField(default=False)

    bowel_movements = models.IntegerField(default=0)

    hunger_times = models.CharField(max_length=10, choices=TIME_CHOICES, blank=True)
    stress_times = models.CharField(max_length=10, choices=TIME_CHOICES, blank=True)
    anxiety_times = models.CharField(max_length=10, choices=TIME_CHOICES, blank=True)
    craving_times = models.CharField(max_length=10, choices=TIME_CHOICES, blank=True)


    def __str__(self):
        return f"Daily Record #{self.id}"
