from django.db import models
from django.core.validators import MinValueValidator

from apps.core.models import Core
from apps.macros_planner.models import MacrosPlanner


class TypeOfDiet(models.TextChoices):
    MAINTENANCE = 'Maintenance', 'Maintenance'
    BULKING = 'Bulking', 'Bulking'
    CUTTING = 'Cutting', 'Cutting'


class Diet(Core):
    macros_planner = models.ForeignKey(MacrosPlanner, on_delete=models.CASCADE, default=None)
    goal = models.CharField(max_length=100, blank=True)
    observations = models.CharField(max_length=300, blank=True)
    initial_date = models.DateField()
    final_date = models.DateField()
    weeks = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    type_of_diet = models.CharField(max_length=50, choices=TypeOfDiet.choices, default=TypeOfDiet.MAINTENANCE)

    @property
    def athlete(self):
        return self.macros_planner.athlete

    @property
    def nutritionist(self):
        return self.macros_planner.nutritionist

    def __str__(self):
        return f"Diet #{self.id}"
