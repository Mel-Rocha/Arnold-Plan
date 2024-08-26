from rest_framework import serializers

from apps.macros_planner.models import MacrosPlanner
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
        fields = ['macros_planner', 'week', 'cho', 'ptn', 'fat', 'kcal', 'kcal_level', 'cho_level', 'ptn_level',
                  'fat_level', 'cho_proportion', 'ptn_proportion', 'fat_proportion']
        extra_kwargs = {'macros_planner': {'read_only': True}, 'week': {'required': False}}


    def create(self, validated_data):
        macros_planner_id = self.context.get('macros_planner_id')
        macros_planner = MacrosPlanner.objects.get(id=macros_planner_id)

        validated_data.pop('macros_planner', None)

        return MacrosSheet.objects.create(macros_planner=macros_planner, **validated_data)


    def to_representation(self, instance):
        """
        Custom representation to include the 'id' of the MacrosSheet.
        """
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        return representation
