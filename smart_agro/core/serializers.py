from rest_framework import serializers
from .models import SoilData, Land, Farmer

class SoilDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilData
        fields = ['id', 'land', 'time', 'N', 'P', 'K', 'S', 'pH', 'moisture']

class LandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Land
        fields = ['id', 'name', 'area', 'address', 'farmer']

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['id', 'name', 'phone','email', 'city','country','postal_code']



class CropsSuggestionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass



