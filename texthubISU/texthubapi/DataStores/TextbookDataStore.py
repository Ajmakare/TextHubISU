from ..serializers import *
from ..models import Textbook
from ..models import Requests

class TextbookDataStore():
    # Get all data (rows) associated with an ISBN
    # We want to retrieve all site info for a single isbn to display to user
    def do_search(ISBN):
        try:
            queryset = Textbook.objects.filter(ISBN = ISBN)
            return queryset
        except:
            print("Could not retrieve textbooks with ISBN: " + ISBN)
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
