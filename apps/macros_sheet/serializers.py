from rest_framework import serializers
from apps.macros_sheet.models import MealMacrosSheet

class MealMacrosSheetSerializer(serializers.ModelSerializer):
    cho = serializers.ReadOnlyField()
    ptn = serializers.ReadOnlyField()
    fat = serializers.ReadOnlyField()
    kcal = serializers.ReadOnlyField()
    cho_proportion = serializers.ReadOnlyField()
    ptn_proportion = serializers.ReadOnlyField()
    fat_proportion = serializers.ReadOnlyField()

    class Meta:
        model = MealMacrosSheet
        fields = ['id', 'meal', 'cho', 'ptn', 'fat', 'kcal', 'cho_proportion', 'ptn_proportion', 'fat_proportion']
