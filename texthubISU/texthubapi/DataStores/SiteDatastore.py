from ..serializers import *
from ..models import *
from itertools import chain
from ..serializers import *
from ..forms import *
from django.shortcuts import render

class SiteDatastore():

    def submit_feedback(feedback):
        try:
            feedback.save()
        except:
            return "Submit Feedback"
        pass