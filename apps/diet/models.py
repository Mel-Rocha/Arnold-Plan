from django.apps import apps
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
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

    def clean(self):
        super().clean()
        overlapping_diets = Diet.objects.filter(
        athlete=self.athlete,
            initial_date__lt=self.final_date,
            final_date__gt=self.initial_date
        ).exclude(id=self.id)

        if overlapping_diets.exists():
            raise ValidationError("The diet dates overlap with another diet for the same athlete.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


@receiver(post_save, sender=Diet)
def create_diet_macros_sheet(sender, instance, created, **kwargs):
    if created:
        DietMacrosSheet = apps.get_model('macros_sheet', 'DietMacrosSheet')
        DietMacrosSheet.objects.create(diet=instance)
        print(f"DietMacrosSheet created for Meal #{instance.id}")
