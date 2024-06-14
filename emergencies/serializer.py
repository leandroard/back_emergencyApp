from rest_framework import serializers
from .models import EmergencyType, Emergency


class EmergenciesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyType
        fields = '__all__'

class EmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency
        fields = '__all__'