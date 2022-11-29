from ..serializers import *
from ..models import *
from itertools import chain
from ..serializers import *
from ..forms import *
from django.shortcuts import render
from ..DataStores.UserDataStore import *
from django.http import HttpResponse, HttpResponseBadRequest


class UserService():
    def add_user_service(request):
        adduser_form = AddUser(request.POST)
        if adduser_form.is_valid():
            User.objects.create_user(
                adduser_form.cleaned_data['Username'], adduser_form.cleaned_data['Email'], adduser_form.cleaned_data['Password'])
            print("Start Service")
            # UserDataStore.add_user(user)
