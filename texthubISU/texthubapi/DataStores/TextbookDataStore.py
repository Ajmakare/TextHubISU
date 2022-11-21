from ..serializers import *
from ..models import Textbook
from itertools import chain
from ..serializers import *
from ..forms import AddISBN
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

    def delete_ISBN():
        pass

    def add_ISBN(request):
        try:
            if request.method == 'POST':
                form = AddISBN(request.POST)
                if form.is_valid():
                    name = form.cleaned_data['name']
                    isbn = form.cleaned_data['ISBN']
                    author = form.cleaned_data['author']

                    example1 = Textbook()
                    example1.ISBN = isbn
                    example1.author = author
                    example1.name = name
                    example1.view_count = 0
                    example1.save()

            form = AddISBN()
            return render(request, 'addisbn.html', {"form": form})
        except:
            return "Add admin failure"

    def update_ISBN():
        pass

    def update_view_count():
        pass

    def submit_review():
        pass
