from django.urls import path, include
from rest_framework import routers
from .views import Views

urlpatterns = [
    path('textbooks/<ISBN>/<sort>', Views.DoSearchView.as_view()),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('admin2', Views.admin, name="admin"),
    # path('login2', views.login, name = "login"),
    path('home', Views.home_view, name='home'),
    path('sendrequest/', Views.sendRequest_view, name = "sendrequest"),
    path('retrieve', Views.RetrieveView.as_view())
]