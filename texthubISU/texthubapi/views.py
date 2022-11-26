from django.shortcuts import *
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import filters

from .serializers import *
from texthubapi.Controllers.TextbookController import *
from texthubapi.Controllers.SiteController import *
from texthubapi.Controllers.ScraperController import *
from .DataStores.ScraperDatastore import *
from .forms import *


def index(request):
    return HttpResponse("Welcome to the ISU TextHub home page!")


# example url: http://127.0.0.1:8000/textbooks/?isbn=testisbn/
class DoSearchView(generics.ListAPIView):
    serializer_class = TextbookSerializer

    def get_queryset(self):
        isbn = self.kwargs['ISBN']
        sort = self.kwargs['sort']
        queryset = TextbookController.do_search_controller(isbn, sort)
        return queryset


def home_view(request):
    try:
        if request.method == 'POST':
            if 'ISBNToReview' in request.POST:
                TextbookController.submit_review_controller(request)
            if 'ISBN' in  request.POST:
                searchisbn_form = SearchISBN(request.POST)
                if searchisbn_form.is_valid():
                    isbn_to_search = searchisbn_form.cleaned_data['ISBN']
                    if 'SortAlphabetical' in request.POST:
                        response = redirect('textbooks/'+isbn_to_search+'/alpha')
                    elif 'SortByPrice' in request.POST:
                        response = redirect('textbooks/'+isbn_to_search+'/price')
                    else:
                        response = redirect('textbooks/'+isbn_to_search+'/default')
                    return response
            if 'FeedbackContent' in request.POST:
                SiteController.submit_feedback_controller(request)
        context = {
            'reviewisbn_form': ReviewISBN,
            'searchisbn_form': SearchISBN,
            'submitfeedback_form': SubmitFeedback
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
            if 'WantToPopulate' in request.POST:
                print('got to call pop')
                ScraperController.populateDB()
        context = {
            'addisbn_form': AddISBN,
            'deleteisbn_form': DeleteISBN,
            'updateisbn_form': UpdateISBN,
            'populate_form': PopulateForm
        }
        return render(request, 'admin.html', context=context)
    except:
        return "Admin page exception"
