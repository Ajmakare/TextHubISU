from unicodedata import decimal
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class ReadingMaterials(models.Model):
    ISBN = models.CharField(max_length=264, unique=True, primary_key=True)
    author = models.CharField(max_length=264)
    name = models.CharField(max_length=264)
    view_count = models.IntegerField(default = 0) 

    class Meta:
        abstract = True

class Textbook(ReadingMaterials):
    ISBN = models.CharField(max_length=264, unique=True, primary_key=True)
    author = models.CharField(max_length=264)
    name = models.CharField(max_length=264)
    view_count = models.IntegerField(default = 0)

class Source(models.Model):
    price = models.DecimalField(max_digits=29, decimal_places=2, default=0.00)
    url = models.CharField(max_length=264)
    ISBN = models.ForeignKey(Textbook, related_name='sources', on_delete = models.CASCADE)

class Review(models.Model):
    review_content = models.CharField(max_length=264)
    ISBN = models.ForeignKey(Textbook, on_delete=models.CASCADE)

class Admin(models.Model):
    username = models.CharField(max_length=264)
    password = models.CharField(max_length=264)

class Feedback(models.Model):
    feedback_content = models.CharField(max_length=264)

class Request(models.Model):
    requestISBN = models.CharField(max_length=264)