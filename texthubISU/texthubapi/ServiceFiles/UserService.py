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
            email = adduser_form.cleaned_data['Email']
            user = adduser_form.cleaned_data['Username']
            if not User.objects.filter(email = email).exists() and not User.objects.filter(username = user).exists():
                print("Start Service")
                User.objects.create_user(
                    user, email, adduser_form.cleaned_data['Password'])
            # UserDataStore.add_user(user)
