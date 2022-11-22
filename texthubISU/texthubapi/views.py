from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics

from .serializers import *
from texthubapi.Controllers.TextbookController import *
from .models import Textbook
from .forms import *

def index(request):
    return HttpResponse("Welcome to the ISU TextHub home page!")


# example url: http://127.0.0.1:8000/textbooks/?isbn=testisbn/
class DoSearchView(generics.ListAPIView):
    serializer_class = TextbookSerializer

    def get_queryset(self):
        isbn = self.kwargs['ISBN']
        queryset = TextbookController.do_search_controller(isbn)
        return queryset

def home_view(request):
    try:
        if request.method == 'POST':
            if 'ISBNToReview' in request.POST:
                TextbookController.submit_review_controller(request)
        context = {
            'reviewisbn_form': ReviewISBN,
        }
        return render(request, 'home.html', context=context)
    except:
        return "Home page exception"


def admin(request):
    print(request.POST)
    print(list(request.POST.items()))
    try:
        if request.method == 'POST':
            if 'ISBNToAdd' in request.POST:
                TextbookController.add_ISBN_controller(request)
            if 'ISBNToDelete' in request.POST:
                TextbookController.delete_ISBN_controller(request)
            if 'ISBNToUpdate' in request.POST:
                TextbookController.update_ISBN_controller(request)
        context = {
            'addisbn_form': AddISBN,
            'deleteisbn_form': DeleteISBN,
            'updateisbn_form':UpdateISBN
        }
        return render(request, 'admin.html', context=context)
    except:
        return "Admin page exception"
