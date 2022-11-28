from ..serializers import *
from ..models import *
from itertools import chain
from ..serializers import *
from ..forms import *
from django.shortcuts import render
from ..DataStores.TextbookDataStore import *
from django.http import HttpResponse, HttpResponseBadRequest
class AdminService():

    def delete_ISBN_service(request):
        deleteisbn_form = DeleteISBN(request.POST)
        if deleteisbn_form.is_valid():
            isbn_from_form = deleteisbn_form.cleaned_data['ISBNToDelete']
            TextbookDataStore.delete_ISBN(isbn_from_form)
        else:
            return "Form invalid"


    def add_admin_service(request):
        addadmin_form = AddAdmin(request.POST)
        if addadmin_form.is_valid():
            login_from_form = addadmin_form.cleaned_data['AdminLogin']
            AdminDataStore.add_admin(login_from_form)
        else:
            return "Form invalid"