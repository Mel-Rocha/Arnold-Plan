from rest_framework import serializers


class CMVColtaco3Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    food_description = serializers.CharField(max_length=1000)
    moisture = serializers.CharField(max_length=200)
    energy_kcal = serializers.CharField(max_length=200)
    energy_kj = serializers.CharField(max_length=200)
    protein = serializers.CharField(max_length=200)
    lipids = serializers.CharField(max_length=200)
    cholesterol = serializers.CharField(max_length=200)
    carbohydrates = serializers.CharField(max_length=200)
    dietary_fiber = serializers.CharField(max_length=200)
    ashes = serializers.CharField(max_length=200)
    category = serializers.CharField(max_length=200)
