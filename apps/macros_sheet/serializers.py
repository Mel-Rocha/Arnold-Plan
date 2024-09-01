from rest_framework import serializers
from apps.macros_sheet.models import MealMacrosSheet, DietMacrosSheet


class MealMacrosSheetSerializer(serializers.ModelSerializer):
    cho = serializers.ReadOnlyField()
    ptn = serializers.ReadOnlyField()
    fat = serializers.ReadOnlyField()
    kcal = serializers.ReadOnlyField()
    cho_proportion = serializers.ReadOnlyField()
    ptn_proportion = serializers.ReadOnlyField()
    fat_proportion = serializers.ReadOnlyField()
    cho_level = serializers.ReadOnlyField()
    ptn_level = serializers.ReadOnlyField()
    fat_level = serializers.ReadOnlyField()
    kcal_level = serializers.ReadOnlyField()

    class Meta:
        model = MealMacrosSheet
        fields = ['id', 'meal', 'cho', 'ptn', 'fat', 'kcal', 'cho_proportion', 'ptn_proportion', 'fat_proportion',
                  'cho_level', 'ptn_level', 'fat_level', 'kcal_level']


class DietMacrosSheetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DietMacrosSheet
        fields = ['id', 'diet', 'cho', 'ptn', 'fat', 'kcal', 'cho_proportion', 'ptn_proportion', 'fat_proportion']
