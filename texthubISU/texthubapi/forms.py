from django import forms


class AddISBN(forms.Form):
    ISBNToAdd = forms.CharField(label="ISBN", max_length=264)
    author = forms.CharField(label="author", max_length=264)
    name = forms.CharField(label="name", max_length=264)


class DeleteISBN(forms.Form):
    ISBNToDelete = forms.CharField(label="ISBN", max_length=264)

class UpdateISBN(forms.Form):
    ISBNToUpdate = forms.CharField(label="ISBN", max_length=264)
    author = forms.CharField(label="author", max_length=264)
    name = forms.CharField(label="name", max_length=264)

class ReviewISBN(forms.Form):
    ISBNToReview = forms.CharField(label = "ISBN", max_length=264)
    ReviewContent = forms.CharField(label = "Review", max_length=264)

class RequestISBN(forms.Form):
    ISBNToRequest = forms.CharField(label = "ISBN", max_length=264)