from ..serializers import *
from ..models import *
from itertools import chain
from ..serializers import *
from ..forms import *
from django.shortcuts import *
from ..DataStores.UserDataStore import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import login
from django.contrib import messages


class UserService():
    def add_user_service(request):
        adduser_form = AddUser(request.POST)
        if adduser_form.is_valid():
            email = adduser_form.cleaned_data['Email']
            user = adduser_form.cleaned_data['Username']
            password = adduser_form.cleaned_data['Password']
            if not User.objects.filter(email=email).exists() and not User.objects.filter(username=user).exists():
                UserDataStore.add_user(user,password,email)
            else:
                return "Duplicate username or email already exists"
        else:
            return "Form Invalid"
            # UserDataStore.add_user(user)

    def login_service(request):
        if request.method == "POST":
            login_form = LoginForm(request.POST)
            print('2...')
            if login_form.is_valid():
                username2 = login_form.cleaned_data['Username']
                password = login_form.cleaned_data['Password']
                print('3...')
                User2 = UserDataStore.read_user(username2)
                if (type(User2) is not str):
                    if (User2.check_password(password)):
                        login(request, User2)
                        return True
                    else:
                        return False
