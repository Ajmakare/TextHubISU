from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics

from .serializers import *
from texthubapi.Controllers.TextbookController import do_search_controller

def index(request):
    return HttpResponse("Welcome to the ISU TextHub home page!")


# example url: http://127.0.0.1:8000/textbooks/?isbn=testisbn/
class DoSearchView(generics.ListAPIView):
    serializer_class = TextbookSerializer
    def get_queryset(self):
        isbn = self.kwargs['ISBN']
        print(isbn)
        queryset = do_search_controller(isbn)
        return queryset
