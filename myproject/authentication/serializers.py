from rest_framework import serializers
from .models import MarketData

class MarketDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketData
        fields = '__all__'  # Include all fields in the model
