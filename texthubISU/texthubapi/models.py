from unicodedata import decimal
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Textbook(models.Model):
    textbookID = models.CharField(max_length=264, unique=True)
    ISBN = models.CharField(max_length=264)
    author = models.CharField(max_length=264)
    name = models.CharField(max_length=264)
    price = models.DecimalField(max_digits=29, decimal_places=2, default=0.00)
    url = models.CharField(max_length=264)
    view_count = models.IntegerField(default = 0)

    def __str__(self):
        return self.textbookID

class Review(models.Model):
    reviewID = models.CharField(max_length=264, unique=True)
    ISBN = models.CharField(max_length=264)
    review_content = models.CharField(max_length=264)
    def __str__(self):
        return self.reviewID

class Admin(models.Model):
    adminID = models.CharField(max_length=264, unique=True)
    username = models.CharField(max_length=264)
    password = models.CharField(max_length=264)
    def __str__(self):
        return self.adminID

class Feedback(models.Model):
    feedbackID = models.CharField(max_length=264, unique=True)
    feedback_content = models.CharField(max_length=264)
    def __str__(self):
        return self.feedbackID

class Requests(models.Model):
    requestID = models.CharField(max_length=264, unique=True)
    requestISBN = models.CharField(max_length=264)