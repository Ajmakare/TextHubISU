from ..serializers import *
from ..models import *
from itertools import chain
from ..serializers import *
from ..forms import *
from django.shortcuts import render

class TextbookDataStore():
    # Get all data (rows) associated with an ISBN
    # We want to retrieve all site info for a single isbn to display to user
    def do_search(param_isbn):
        try:
            queryset = Textbook.objects.filter(ISBN = param_isbn).prefetch_related('sources').all()
            return queryset
        except:
            print("Could not retrieve textbooks with ISBN: " + param_isbn)
            pass

    def request_ISBN():
        pass

    def retrieve_all_textBooks():
        try:
            queryset = Textbook.objects.all()
            return queryset
        except:
            print("Could not retrieve textbooks")
            pass

    def delete_ISBN(isbn):
        try:
            Textbook.objects.filter(ISBN=isbn).delete()
        except:
            return "Delete ISBN exception"

    def add_ISBN(textbook):
        try:
            textbook.save()
        except:
            return "Add ISBN exception"

    def update_ISBN(textbook):
        try:
            textbook.save()
        except:
            return "Update ISBN exception"

    def update_view_count():
        pass

    def submit_review(review):
        try:
            review.save()
        except:
            return "Submit review exception"
    # def add_isbn2 ():
