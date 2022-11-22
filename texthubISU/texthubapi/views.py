from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics

from .serializers import *
from texthubapi.Controllers.TextbookController import *
from .models import Textbook
from .forms import AddISBN
from .forms import DeleteISBN


def index(request):
    return HttpResponse("Welcome to the ISU TextHub home page!")


# example url: http://127.0.0.1:8000/textbooks/?isbn=testisbn/
class DoSearchView(generics.ListAPIView):
    serializer_class = TextbookSerializer

    def get_queryset(self):
        isbn = self.kwargs['ISBN']
        queryset = TextbookController.do_search_controller(isbn)
        return queryset


def admin(request):

    addisbn_form = AddISBN()
    deleteisbn_form = DeleteISBN()
    print(request.POST)
    print(list(request.POST.items()))
    try:
        if request.method == 'POST':
            if 'ISBNToAdd' in request.POST:
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
            if 'ISBNToDelete' in request.POST:
                print('delete pls')
                deleteisbn_form = DeleteISBN(request.POST)
                if deleteisbn_form.is_valid():
                    isbn_from_form = deleteisbn_form.cleaned_data['ISBNToDelete']

                    Textbook.objects.filter(ISBN=isbn_from_form).delete()
        context = {
            'addisbn_form': AddISBN,
            'deleteisbn_form': DeleteISBN
        }

        return render(request, 'admin.html', context=context)
    except:
        return "Add admin failure"
