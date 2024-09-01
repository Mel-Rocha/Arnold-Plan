from rest_framework import serializers
from apps.macros_sheet.models import MealMacrosSheet, DietMacrosSheet


MACROS_SHEETS_FIELDS = [
    'id', 'cho', 'ptn', 'fat', 'kcal', 'cho_proportion', 'ptn_proportion', 'fat_proportion',
    'cho_level', 'ptn_level', 'fat_level', 'kcal_level'
]

class MealMacrosSheetSerializer(serializers.ModelSerializer):

    class Meta:
        model = MealMacrosSheet
        fields = MACROS_SHEETS_FIELDS
        read_only_fields = MACROS_SHEETS_FIELDS


class DietMacrosSheetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DietMacrosSheet
        fields = ['id', 'diet', 'cho', 'ptn', 'fat', 'kcal', 'cho_proportion', 'ptn_proportion', 'fat_proportion']
