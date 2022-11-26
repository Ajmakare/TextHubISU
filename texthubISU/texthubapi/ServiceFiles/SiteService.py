from ..serializers import *
from ..models import Feedback
from itertools import chain
from ..serializers import *
from ..forms import *
from django.shortcuts import render
from ..DataStores.SiteDatastore import *
class SiteService():
    def submit_Feedback_service(request):

        submitfeedback_form = SubmitFeedback(request.POST)
        if submitfeedback_form.is_valid():
            review = submitfeedback_form.cleaned_data['FeedbackContent']

            example = Feedback(feedback_content=review)

            # example.feedback_content = review

            SiteDatastore.submit_feedback(example)
        else:
            return "Form invalid"

    # planning on using this when searching for textbooks is done :D
    # def update_ISBN_viewcount_service(request):
    #         TextbookDataStore.update_ISBN_viewcount(isbn)
    #     else:
    #         return "Form invalid"