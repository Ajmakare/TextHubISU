from django.urls import path, include
from rest_framework import routers
from . import views

urlpatterns = [
    path('textbooks/<ISBN>/<sort>', views.DoSearchView.as_view()),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('admin2/', views.admin, name="admin2"),
    path('login2/', views.loginView, name="login"),
    path('home', views.home_view, name='home'),
    path('sendrequest/', views.sendRequest_view, name="sendrequest"),
    path('retrieve', views.retrieveView.as_view())
]
