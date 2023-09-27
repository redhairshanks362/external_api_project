from tvshow.models import TVShow, AllTvShows
from rest_framework import serializers

class TVShowSerializers(serializers.ModelSerializer):
    class Meta:
        model = TVShow
        fields = '__all__'

class AllTvShowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllTvShows
        fields = ['shows']