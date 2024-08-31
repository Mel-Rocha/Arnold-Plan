from rest_framework import serializers
from apps.diet.models import Diet
from apps.macros_sheet.models import MacrosSheet

class MacrosSheetSerializer(serializers.ModelSerializer):
    kcal = serializers.ReadOnlyField()
    kcal_level = serializers.ReadOnlyField()
    cho_level = serializers.ReadOnlyField()
    ptn_level = serializers.ReadOnlyField()
    fat_level = serializers.ReadOnlyField()
    cho_proportion = serializers.ReadOnlyField()
    ptn_proportion = serializers.ReadOnlyField()
    fat_proportion = serializers.ReadOnlyField()

    class Meta:
        model = MacrosSheet
        fields = ['diet', 'week', 'cho', 'ptn', 'fat', 'kcal', 'kcal_level', 'cho_level', 'ptn_level',
                  'fat_level', 'cho_proportion', 'ptn_proportion', 'fat_proportion']
        extra_kwargs = {'diet': {'read_only': True}, 'week': {'required': False}}

    def create(self, validated_data):
        diet_id = self.context.get('diet_id')
        diet = Diet.objects.get(id=diet_id)

        validated_data.pop('diet', None)

        return MacrosSheet.objects.create(diet=diet, **validated_data)

    def to_representation(self, instance):
        """
        Custom representation to include the 'id' of the MacrosSheet.
        """
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        return representation