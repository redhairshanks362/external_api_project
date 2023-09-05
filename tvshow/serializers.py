from tvshow.models import TVShow
from rest_framework import serializers

class TVShowSerializers(serializers.ModelSerializer):
    class Meta:
        model = TVShow
        fields = '__all__'