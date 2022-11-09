from unicodedata import decimal
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Textbook(models.Model):
    ISBN = models.CharField(max_length=264, unique=True, primary_key=True)
    author = models.CharField(max_length=264)
    name = models.CharField(max_length=264)
    view_count = models.IntegerField(default = 0)
    def __str__(self):
        return self.ISBN

class Source(models.Model):
    sourceID = models.CharField(max_length=264, unique=True, primary_key=True)
    price = models.DecimalField(max_digits=29, decimal_places=2, default=0.00)
    url = models.CharField(max_length=264)
    ISBN = models.CharField(max_length=264, default = '')
    def __str__(self):
        return self.sourceID

class Review(models.Model):
    reviewID = models.CharField(max_length=264, unique=True, primary_key=True)
    review_content = models.CharField(max_length=264)
    ISBN = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    def __str__(self):
        return self.reviewID

class Admin(models.Model):
    adminID = models.CharField(max_length=264, unique=True, primary_key=True)
    username = models.CharField(max_length=264)
    password = models.CharField(max_length=264)
    def __str__(self):
        return self.adminID

class Feedback(models.Model):
    feedbackID = models.CharField(max_length=264, unique=True, primary_key=True)
    feedback_content = models.CharField(max_length=264)
    def __str__(self):
        return self.feedbackID

class Request(models.Model):
    requestID = models.CharField(max_length=264, unique=True, primary_key=True)
    requestISBN = models.CharField(max_length=264)