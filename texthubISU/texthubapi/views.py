from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

from .serializers import *
from texthubapi.Controllers.TextbookController import do_search_controller

def index(request):
    return HttpResponse("Welcome to the ISU TextHub home page!")

class DoSearchView(viewsets.ModelViewSet):
    queryset = do_search_controller("testisbn")
    serializer_class = TextbookSerializer
