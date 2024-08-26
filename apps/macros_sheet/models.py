import logging

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.core.validators import MinValueValidator

from apps.core.models import Core
from apps.macros_planner.models import MacrosPlanner
from apps.macros_sheet.calcs import KcalLevel, CalcMacroLevel, ProportionGKG


logger = logging.getLogger(__name__)


class MacrosSheet(Core):
    macros_planner = models.ForeignKey(MacrosPlanner, related_name='macros_sheets', on_delete=models.CASCADE)
    week = models.PositiveIntegerField(default=0)
    cho = models.FloatField(default=1, validators=[MinValueValidator(1)])
    ptn = models.FloatField(default=1, validators=[MinValueValidator(1)])
    fat = models.FloatField(default=1, validators=[MinValueValidator(1)])
    kcal = models.FloatField(default=0)

    @property
    def athlete(self):
        return self.macros_planner.athlete

    @property
    def weight(self):
        return self.athlete.weight

    @property
    def kcal_level(self):
        return KcalLevel.calculate_kcal_level(self.kcal)

    @property
    def cho_level(self):
        return CalcMacroLevel().calculate_macro_level(self.cho, self.kcal, 'cho')

    @property
    def ptn_level(self):
        return CalcMacroLevel().calculate_macro_level(self.ptn, self.kcal, 'ptn')

    @property
    def fat_level(self):
        return CalcMacroLevel().calculate_macro_level(self.fat, self.kcal, 'fat')

    @property
    def cho_proportion(self):
        proportions = ProportionGKG(self.weight, self.cho, self.ptn, self.fat)
        return round(proportions.cho_proportion, 2)

    @property
    def ptn_proportion(self):
        proportions = ProportionGKG(self.weight, self.cho, self.ptn, self.fat)
        return round(proportions.ptn_proportion, 2)

    @property
    def fat_proportion(self):
        proportions = ProportionGKG(self.weight, self.cho, self.ptn, self.fat)
        return round(proportions.fat_proportion, 2)


    def update_week_based_on_id(self):
        if self.week == 0 and self.macros_planner:
            macros_sheets = self.macros_planner.macros_sheets.all().order_by('id')

            for index, macros_sheet in enumerate(macros_sheets):
                macros_sheet.week = index + 1
                macros_sheet.save()

            new_week = macros_sheets.last().week + 1 if macros_sheets.exists() else 1
            self.week = new_week
            self.macros_planner.save()


    def save(self, *args, **kwargs):
        self.kcal = KcalLevel.calculate_kcal(self.cho, self.ptn, self.fat)
        super().save(*args, **kwargs)
        self.update_week_based_on_id()


@receiver(pre_delete, sender=MacrosSheet)
def pre_delete_macros_sheet(sender, instance, **kwargs):
    logger.info(f"Signal received for MacrosSheet {instance.id} deletion.")
    instance.update_week_based_on_id()
