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
        pass

    def delete_ISBN(request):
        try:
            print('delete pls')
            deleteisbn_form = DeleteISBN(request.POST)
            if deleteisbn_form.is_valid():
                isbn_from_form = deleteisbn_form.cleaned_data['ISBNToDelete']

                Textbook.objects.filter(ISBN=isbn_from_form).delete()
        except:
            return "Delete ISBN exception"

    def add_ISBN(request):
        try:
            print('add the isbn pls')
            addisbn_form = AddISBN(request.POST)
            if addisbn_form.is_valid():
                name = addisbn_form.cleaned_data['name']
                isbn = addisbn_form.cleaned_data['ISBNToAdd']
                author = addisbn_form.cleaned_data['author']

                example1 = Textbook()
                example1.ISBN = isbn
                example1.author = author
                example1.name = name
                example1.view_count = 0
                print("add an isbn")
                example1.save()
        except:
            return "Add ISBN exception"

    def update_ISBN():
        pass

    def update_view_count():
        pass

    def submit_review(request):
        try:
            reviewisbn_form = ReviewISBN(request.POST)
            if reviewisbn_form.is_valid():
                isbn_review = reviewisbn_form.cleaned_data['ISBNToReview']
                review = reviewisbn_form.cleaned_data['ReviewContent']

                new_review = Review(review_content=review, ISBN = Textbook.objects.get(pk = isbn_review))
                new_review.save()
        except:
            return "Submit review exception"
