from rest_framework import serializers

from .models import Textbook

class TextbookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Textbook
        fields = ('textbookID', 'ISBN', 'author','name','price','url','view_count')