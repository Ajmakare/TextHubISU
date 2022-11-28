from ..serializers import *
from ..models import *
from itertools import chain
from ..serializers import *
from ..forms import *
from django.shortcuts import render
from ..DataStores.TextbookDataStore import *
from django.http import HttpResponse, HttpResponseBadRequest


class TextbookService():

    def retrieve_all_textBooks_service():
        return TextbookDataStore.retrieve_all_textBooks()

    def delete_ISBN_service(request):
        deleteisbn_form = DeleteISBN(request.POST)
        if deleteisbn_form.is_valid():
            isbn_from_form = deleteisbn_form.cleaned_data['ISBNToDelete']
            TextbookDataStore.delete_ISBN(isbn_from_form)
        else:
            return "Form invalid"

    def add_ISBN_service(request):
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
            TextbookDataStore.add_ISBN(example1)
        else:
            return "Form invalid"

    def update_ISBN_service(request):
        updateisbn_form = UpdateISBN(request.POST)
        if updateisbn_form.is_valid():
            new_name = updateisbn_form.cleaned_data['name']
            isbn = updateisbn_form.cleaned_data['ISBNToUpdate']
            new_author = updateisbn_form.cleaned_data['author']
            if Textbook.objects.filter(pk=isbn).exists():
                updated_textbook = Textbook.objects.get(pk=isbn)
                print(str(updated_textbook))
                updated_textbook.name = new_name
                updated_textbook.author = new_author  
                TextbookDataStore.update_ISBN(updated_textbook)    
        else:
            return "Form invalid"  
    
    def submit_review_service(request):
        reviewisbn_form = ReviewISBN(request.POST)
        if reviewisbn_form.is_valid():
            isbn_review = reviewisbn_form.cleaned_data['ISBNToReview']
            review = reviewisbn_form.cleaned_data['ReviewContent']

            new_review = Review(review_content=review, ISBN = Textbook.objects.get(pk = isbn_review))
            TextbookDataStore.submit_review(new_review)
        else:
            return "Invalid form"


    def request_ISBN_service(request):
        requestisbn_form = RequestISBN(request.POST)
        if requestisbn_form.is_valid():
            isbn_request = requestisbn_form.cleaned_data['ISBNToRequest']

            new_request = Request(requestISBN = isbn_request)
            TextbookDataStore.request_ISBN(new_request)

