from django.db import models
from django.core.validators import MinValueValidator

from apps.core.models import Core
from apps.user.models import Athlete, Nutritionist


class MacrosPlanner(Core):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE)
    goal = models.CharField(max_length=100, blank=True)
    initial_date = models.DateField()
    final_date = models.DateField()
    weeks = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"MacrosPlanner #{self.id}"
