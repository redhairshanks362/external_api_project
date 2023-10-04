from wordOfTheDay.models import WordModel
from rest_framework import serializers
#H
class WordSerializers(serializers.ModelSerializer):
    class Meta:
        model = WordModel
        fields = '__all__'