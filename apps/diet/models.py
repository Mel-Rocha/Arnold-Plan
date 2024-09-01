from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        DailyRecords = apps.get_model('daily_records', 'DailyRecords')
        daily_records = DailyRecords.objects.filter(athlete=self.athlete)
        if daily_records.exists():
            earliest_record = daily_records.order_by('date').first().date
            latest_record = daily_records.order_by('date').last().date

            if self.initial_date > earliest_record:
                raise ValidationError(f"Initial date cannot be after the earliest daily record date: {earliest_record}")
            if self.final_date < latest_record:
                raise ValidationError(f"Final date cannot be before the latest daily record date: {latest_record}")


@receiver(post_save, sender=Diet)
def create_diet_macros_sheet(sender, instance, created, **kwargs):
    if created:
        DietMacrosSheet = apps.get_model('macros_sheet', 'DietMacrosSheet')
        DietMacrosSheet.objects.create(diet=instance)
        print(f"DietMacrosSheet created for Meal #{instance.id}")
