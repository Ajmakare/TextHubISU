from django import forms


class AddISBN(forms.Form):
    ISBN = forms.CharField(label="ISBN", max_length=264)
    author = forms.CharField(label="author", max_length=264)
    name = forms.CharField(label="name", max_length=264)
