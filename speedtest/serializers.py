from speedtest.models import SpeedTest
from rest_framework import serializers

class STSerializers(serializers.ModelSerializer):
     binary_url = serializers.SerializerMethodField()

     class Meta:
         model = SpeedTest
         fields = '__all__'

     def get_binary_url(self,obj):
         url = obj.BinaryUrl
         return self.context['request'].build_absolute_uri(url)