from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics

from .serializers import *
from texthubapi.Controllers.TextbookController import do_search_controller
from .models import Textbook
from .forms import AddISBN


def index(request):
    return HttpResponse("Welcome to the ISU TextHub home page!")


# example url: http://127.0.0.1:8000/textbooks/?isbn=testisbn/
class DoSearchView(generics.ListAPIView):
    serializer_class = TextbookSerializer

    def get_queryset(self):
        isbn = self.kwargs['ISBN']
        queryset = do_search_controller(isbn)
        return queryset


def addisbn(request):
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
