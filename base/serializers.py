from rest_framework import serializers
from .models import NASAApod

class ApodSerializer(serializers.ModelSerializer):
    class Meta:
        model = NASAApod
        fields = '__all__'
