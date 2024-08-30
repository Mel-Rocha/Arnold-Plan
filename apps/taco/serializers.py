from rest_framework import serializers

class CMVColtaco3Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    descricaoalimento = serializers.CharField(max_length=1000)
    umidade = serializers.CharField(max_length=200)
    energiakcal = serializers.CharField(max_length=200)
    energiakj = serializers.CharField(max_length=200)
    proteina = serializers.CharField(max_length=200)
    lipideos = serializers.CharField(max_length=200)
    colesterol = serializers.CharField(max_length=200)
    carboidrato = serializers.CharField(max_length=200)
    fibraalimentar = serializers.CharField(max_length=200)
    cinzas = serializers.CharField(max_length=200)
    categoria = serializers.CharField(max_length=200)