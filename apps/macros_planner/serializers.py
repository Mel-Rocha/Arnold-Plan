from rest_framework import serializers

from apps.user.models import Nutritionist
from apps.macros_sheet.models import MacrosSheet
from apps.diet.serializers import DietSerializer
from apps.macros_planner.models import MacrosPlanner


class MacrosPlannerSerializer(serializers.ModelSerializer):
    diets = DietSerializer(many=True, required=False)

    class Meta:
        model = MacrosPlanner
        fields = '__all__'
        extra_kwargs = {
            'nutritionist': {'read_only': True},
        }

    def create(self, validated_data):
        diets_data = validated_data.pop('diets', [])

        user = self.context['request'].user

        try:
            nutritionist = Nutritionist.objects.get(user=user)
        except Nutritionist.DoesNotExist:
            raise serializers.ValidationError({'nutritionist': 'Nutritionist with the current user does not exist.'})

        macros_planner = MacrosPlanner.objects.create(nutritionist=nutritionist, **validated_data)

        weeks = validated_data.get('weeks', 0)
        for week in range(1, weeks + 1):
            MacrosSheet.objects.create(macros_planner=macros_planner, week=week)

        context = self.context
        context['macros_planner_id'] = macros_planner.id

        for diet_data in diets_data:
            diet_data['macros_planner'] = macros_planner.id

            diet_serializer = DietSerializer(data=diet_data, context=context)
            if diet_serializer.is_valid():
                diet_serializer.save()
            else:
                raise serializers.ValidationError(diet_serializer.errors)

        return macros_planner
