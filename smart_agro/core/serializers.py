from rest_framework import serializers
from .models import SoilData

class SoilDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilData
        fields = ['id', 'land', 'time', 'N', 'P', 'K', 'S', 'pH', 'moisture']
