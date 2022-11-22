from rest_framework import serializers

from .models import *

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ("__all__")

class TextbookSerializer(serializers.ModelSerializer):
    sources = SourceSerializer(read_only=True,many=True)
    class Meta:
        model = Textbook
        fields = ("__all__")