import logging

from django.db import models
from django.core.validators import MinValueValidator

from apps.core.models import Core
from apps.diet.models import Diet
from apps.macros_sheet.calcs import KcalLevel, CalcMacroLevel, ProportionGKG
from apps.meal.models import Meal

logger = logging.getLogger(__name__)


class MealMacrosSheet(Core):
    meal = models.OneToOneField(Meal, related_name='macros_sheet', on_delete=models.CASCADE)

    @property
    def cho(self):
        """Calcula o total de carboidratos (CHO) da refeição."""
        return sum(food['carbohydrates'] for food in self.meal.foods)

    @property
    def ptn(self):
        """Calcula o total de proteínas (PTN) da refeição."""
        return sum(food['protein'] for food in self.meal.foods)

    @property
    def fat(self):
        """Calcula o total de gorduras (FAT) da refeição."""
        return sum(food['lipids'] for food in self.meal.foods)

    @property
    def kcal(self):
        """Calcula o total de calorias (KCAL) da refeição."""
        return sum(food['energy_kcal'] for food in self.meal.foods)

    @property
    def cho_proportion(self):
        """Calcula a proporção de carboidratos (CHO) em relação ao peso do atleta."""
        proportions = ProportionGKG(self.meal.diet.athlete.weight, self.cho, self.ptn, self.fat)
        return round(proportions.cho_proportion, 2)

    @property
    def ptn_proportion(self):
        """Calcula a proporção de proteínas (PTN) em relação ao peso do atleta."""
        proportions = ProportionGKG(self.meal.diet.athlete.weight, self.cho, self.ptn, self.fat)
        return round(proportions.ptn_proportion, 2)

    @property
    def fat_proportion(self):
        """Calcula a proporção de gorduras (FAT) em relação ao peso do atleta."""
        proportions = ProportionGKG(self.meal.diet.athlete.weight, self.cho, self.ptn, self.fat)
        return round(proportions.fat_proportion, 2)



