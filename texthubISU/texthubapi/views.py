from django.shortcuts import *
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse
from django.views.generic.list import ListView
from rest_framework import generics
from rest_framework import filters
from django.views.generic.list import ListView
from json import loads as jloads

from .serializers import *
from texthubapi.Controllers.TextbookController import *
from texthubapi.Controllers.SiteController import *
from texthubapi.Controllers.ScraperController import *
from texthubapi.Controllers.UserController import *
from .forms import *
from django.contrib import messages  # import messages
from django.contrib.auth import login
from texthubapi.scraperstuff.scraper import main
import threading


def index(request):
    return HttpResponse("Welcome to the ISU TextHub home page!")


# example url: http://127.0.0.1:8000/textbooks/?isbn=testisbn/
class DoSearchView(ListView):
    allow_empty = False
    template_name = 'searchresults.html'
    context_object_name = 'textbooks'

    def get_queryset(self):
        isbn = self.kwargs['ISBN']
        sort = self.kwargs['sort']
        queryset = TextbookController.do_search_controller(isbn, sort)
        # TextbookController.update_view_count_controller(isbn)
        return queryset


def home_view(request):
    try:
        if request.method == 'POST':
            if 'ISBNToReview' in request.POST:
                try:
                    TextbookController.submit_review_controller(request)
                    messages.success(request, 'Submit review success!')
                except:
                    messages.error(request, 'Submit review failed :(')
            if 'ISBN' in request.POST:
                searchisbn_form = SearchISBN(request.POST)
                if searchisbn_form.is_valid():
                    isbn_to_search = searchisbn_form.cleaned_data['ISBN']
                    # If a user has both sort boxes checked, error must be thrown
                    if searchisbn_form.cleaned_data['SortAlphabetical'] == True and searchisbn_form.cleaned_data['SortByPrice'] == True:
                        messages.error(
                            request, 'Please select only 1 sort method')
                        return redirect('home')
                    # If the user searches an ISBN not in our database, redirect to submit request view
                    elif not Textbook.objects.filter(pk=isbn_to_search).exists():
                        request.session['isbn_to_request'] = request.POST
                        return redirect('sendrequest')
                    # Return results alphabetically
                    elif 'SortAlphabetical' in request.POST:
                        response = redirect(
                            'textbooks/'+isbn_to_search+'/alpha')
                    # Return results by price
                    elif 'SortByPrice' in request.POST:
                        response = redirect(
                            'textbooks/'+isbn_to_search+'/price')
                    # Else, return results by default (ID order)
                    else:
                        response = redirect(
                            'textbooks/'+isbn_to_search+'/default')
                    TextbookDataStore.update_view_count(isbn_to_search)
                    return response
            if 'FeedbackContent' in request.POST:
                try:
                    SiteController.submit_feedback_controller(request)
                    messages.success(request, 'Submit feedback success!')
                except:
                    messages.error(request, 'Submit feedback failed :(')
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
    print(request.user.is_authenticated)
    try:
        if request.method == 'POST':
            if 'ISBNToAdd' in request.POST:
                try:
                    TextbookController.add_ISBN_controller(request)
                    messages.success(request, 'ISBN Added to database!')
                except:
                    messages.error(request, 'Could not add ISBN to database!')
            if 'ISBNToDelete' in request.POST:
                try:
                    TextbookController.delete_ISBN_controller(request)
                    messages.success(request, 'ISBN deleted from database!')
                except:
                    messages.error(
                        request, 'Could not delete ISBN from database!')
            if 'ISBNToUpdate' in request.POST:
                try:
                    TextbookController.update_ISBN_controller(request)
                    messages.success(request, 'ISBN updated in database!')
                except:
                    messages.error(
                        request, 'ISBN not in database!')
            if 'WantToPopulate' in request.POST:
                print('got to call pop')
                ScraperController.scrape_controller()
            if "Email" in request.POST:
                try:
                    UserController.add_user_controller(request)
                    messages.success(request, 'User created successfully!')
                except:
                    messages.error(
                        request, 'Could not create user!')

        context = {
            'addisbn_form': AddISBN,
            'deleteisbn_form': DeleteISBN,
            'updateisbn_form': UpdateISBN,
            'populate_form': PopulateForm,
            'register_form': AddUser
        }
        return render(request, 'admin.html', context=context)
    except:
        return "Admin page exception"


def sendRequest_view(request):
    try:
        if request.method == 'POST':
            if 'RequestButton' in request.POST:
                try:
                    isbn_to_request = request.session.get('isbn_to_request')
                    TextbookController.request_ISBN_controller(isbn_to_request)
                    messages.success(request, 'Submit request success!')
                except:
                    messages.error(request, 'Submit request failed :(')
        return render(request, 'sendrequest.html', context={'requestisbn_form': RequestISBN})
    except:
        return "Could not request an ISBN"


class retrieveView(ListView):
    allow_empty = False
    template_name = 'retrieve.html'
    context_object_name = 'textbooks'

    def get_queryset(self):
        queryset = TextbookController.retrieve_all_textBooks_controller()
        # TextbookController.update_view_count_controller(isbn)
        return queryset


def login_view(request):

    if request.method == 'POST':

        if (UserController.login_controller(request)):
            return redirect('admin2')
        else:
            messages.error(request, "Username or password was incorrect!")

    return render(request, 'login.html', context={'login_form': LoginForm})
