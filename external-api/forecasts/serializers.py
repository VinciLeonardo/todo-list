from rest_framework import serializers


class ForecastDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    condition = serializers.CharField()
    temperature_celsius = serializers.IntegerField()
    good_for_outdoor = serializers.BooleanField()