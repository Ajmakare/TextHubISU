import threading
from ..serializers import *
from ..models import Textbook
from ..models import Request
from itertools import chain
from ..serializers import *
from ..forms import *
from django.shortcuts import *
from django.db.models import Prefetch, F
from django.db.models.functions import Lower
from ..scraperstuff.scraper import main


class TextbookDataStore():
    # Get all data (rows) associated with an ISBN
    # We want to retrieve all site info for a single isbn to display to user
    def do_search(param_isbn, sort):
        try:
            if sort == 'alpha':
                queryset = {'bookinfos': Textbook.objects.filter(ISBN=param_isbn),
                            'sources': Source.objects.filter(ISBN=param_isbn).order_by(Lower('url'))}
                return queryset
            if sort == 'price':
                queryset = {'bookinfos': Textbook.objects.filter(ISBN=param_isbn),
                            'sources': Source.objects.filter(ISBN=param_isbn).order_by('price')}
                return queryset
            else:
                queryset = {'bookinfos': Textbook.objects.filter(ISBN=param_isbn),
                            'sources': Source.objects.filter(ISBN=param_isbn)}
            return queryset

        except:
            print("Could not retrieve textbooks with ISBN: " + param_isbn)
            pass

    # send an ISBN to be listed on the admin page
    def request_ISBN(request_isbn):
        try:
            request_isbn.save()
        except:
            raise AttributeError

    def retrieve_all_textBooks():
        try:
            queryset = {'bookinfos': Textbook.objects.all()}
            return queryset
        except:
            print("Could not retrieve textbooks")
            pass

    def delete_ISBN(isbn):
        if Textbook.objects.filter(pk=isbn).exists():
            Textbook.objects.filter(pk=isbn).delete()
        else:
            raise ValueError

    def add_ISBN(textbook):
        try:  # check for duplicates
            if not Textbook.objects.filter(pk=textbook.ISBN).exists():
                textbook.save()
        except:
            return "Add ISBN exception"

    def update_ISBN(textbook):
        try:
            textbook.save()
        except:
            raise AttributeError

    def update_view_count(isbn):
        try:
            Textbook.objects.filter(ISBN=isbn).update(
                view_count=F('view_count') + 1)
        except:
            return "Update view count exception"
        # pass

    def submit_review(review):
        try:
            review.save()
        except:
            raise AttributeError
    # def add_isbn2 ():
            return "Submit review exception"

    def add_source(source, param_url):
        try:  # check for duplicates
            if not Source.objects.filter(url=param_url).exists():
                source.save()
        except:
            return "Add ISBN exception"
