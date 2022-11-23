from django import forms

class SearchISBN(forms.Form):
    ISBN = forms.CharField(label="ISBN", max_length=264)

class SearchISBN(forms.Form):
    ISBN = forms.CharField(label="ISBN", max_length=264)

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
    ISBNToReview = forms.CharField(label="ISBN", max_length=264)
    ReviewContent = forms.CharField(label="Review", max_length=264)


class SubmitFeedback(forms.Form):
    FeedbackContent = forms.CharField(label="Feedback", max_length=264)


class PopulateForm(forms.Form):
    WantToPopulate = forms.BooleanField(label="choice")
