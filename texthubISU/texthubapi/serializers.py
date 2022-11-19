from rest_framework import serializers

from .models import *

class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = ("__all__")

class TextbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Textbook
        fields = ("__all__")