from ..serializers import *
from ..models import Textbook
<<<<<<< HEAD
from ..models import Requests
=======
from itertools import chain
>>>>>>> 0b44d790ddb2bae86552231af2aae9931ba19a99

class TextbookDataStore():
    # Get all data (rows) associated with an ISBN
    # We want to retrieve all site info for a single isbn to display to user
    def do_search(param_isbn):
        try:
            queryset = Textbook.objects.filter(ISBN=param_isbn)
            return queryset
        except:
            print("Could not retrieve textbooks with ISBN: " + param_isbn)
            pass
    
    #send an ISBN to be listed on the admin page
    def request_ISBN(ISBN):
        try:
            ISBNreq = Requests(RequestISBN = ISBN)
            return ISBNreq
        except:
            print("Could not request an ISBN")
            pass

    def retrieve_all_textBooks():
        pass

    def delete_ISBN():
        pass

    def add_ISBN():
        pass

    def update_ISBN():
        pass

    def update_view_count():
        pass

    def submit_review():
        pass
