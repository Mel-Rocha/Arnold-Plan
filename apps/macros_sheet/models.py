import logging

from django.db import models
from django.core.validators import MinValueValidator

from apps.core.models import Core
from apps.diet.models import Diet
from apps.macros_sheet.calcs import KcalLevel, CalcMacroLevel, ProportionGKG


logger = logging.getLogger(__name__)


class MacrosSheet(Core):
    diet = models.ForeignKey(Diet, related_name='macros_sheets', on_delete=models.CASCADE)
    cho = models.FloatField(default=1, validators=[MinValueValidator(1)])
    ptn = models.FloatField(default=1, validators=[MinValueValidator(1)])
    fat = models.FloatField(default=1, validators=[MinValueValidator(1)])
    kcal = models.FloatField(default=0)

    @property
    def athlete(self):
        return self.diet.athlete

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


    def save(self, *args, **kwargs):
        self.kcal = KcalLevel.calculate_kcal(self.cho, self.ptn, self.fat)
        super().save(*args, **kwargs)

