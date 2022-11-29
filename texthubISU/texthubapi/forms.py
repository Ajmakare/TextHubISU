from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchISBN(forms.Form):
    ISBN = forms.CharField(label="Type ISBN to Search", max_length=264)
    SortAlphabetical = forms.BooleanField(
        label="Sort Sources Alphabetically", required=False)
    SortByPrice = forms.BooleanField(
        label="Sort Sources by Price (Low to high)", required=False)

class AddISBN(forms.Form):
    ISBNToAdd = forms.CharField(label="ISBN to Add", max_length=264)
    name = forms.CharField(label="Name", max_length=264)
    author = forms.CharField(label="Author", max_length=264)


class DeleteISBN(forms.Form):
    ISBNToDelete = forms.CharField(label="ISBN to Delete", max_length=264)


class UpdateISBN(forms.Form):
    ISBNToUpdate = forms.CharField(label="ISBN to Update", max_length=264)
    name = forms.CharField(label="Name", max_length=264)
    author = forms.CharField(label="Author", max_length=264)


class ReviewISBN(forms.Form):
    ISBNToReview = forms.CharField(label="Type ISBN to Review", max_length=264)
    ReviewContent = forms.CharField(label="Review", max_length=264)


class SubmitFeedback(forms.Form):
    FeedbackContent = forms.CharField(
        label="Leave Site Feedback", max_length=264)


class PopulateForm(forms.Form):
    WantToPopulate = forms.BooleanField(label="choice")


class RequestISBN(forms.Form):
    ISBNToRequest = forms.CharField(label="ISBN", max_length=264)


class Login(forms.Form):
    Username = forms.CharField(label="username", max_length=264)
    Password = forms.CharField(label="password", max_length=264)

class AddUser(forms.Form):
    Email = forms.EmailField(required=True)
    Username = forms.CharField(label="username", max_length=264)
    Password = forms.CharField(label="password", max_length=264)

