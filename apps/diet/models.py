from django.db import models
from django.core.validators import MinValueValidator

from apps.core.models import Core
from apps.user.models import Athlete, Nutritionist


class TypeOfDiet(models.TextChoices):
    MAINTENANCE = 'Maintenance', 'Maintenance'
    BULKING = 'Bulking', 'Bulking'
    CUTTING = 'Cutting', 'Cutting'


class Diet(Core):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE)
    goal = models.CharField(max_length=100, blank=True)
    observations = models.CharField(max_length=300, blank=True)
    initial_date = models.DateField()
    final_date = models.DateField()
    weeks = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    type_of_diet = models.CharField(max_length=50, choices=TypeOfDiet.choices, default=TypeOfDiet.MAINTENANCE)


    def __str__(self):
        return f"Diet #{self.id}"
