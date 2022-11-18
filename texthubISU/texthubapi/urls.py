from django.urls import path, include
from rest_framework import routers
from . import views

urlpatterns = [
    path('textbooks/<ISBN>/', views.DoSearchView.as_view()),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('addisbn', views.addisbn, name="add_isbn"),
]
