from rest_framework import serializers

from .models import *

class TextbookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Textbook
        fields = ("__all__")