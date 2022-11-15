from ..serializers import *
from ..models import Textbook

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

    def request_ISBN():
        pass

    def retrieve_all_textBooks():
        try:
            queryset = Textbook.objects.all()
            return queryset
        except:
            print("Could not retrieve textbooks")
            pass

    def delete_ISBN(ISBN):
        try:
            queryset = Textbook.objects.filter(ISBN = ISBN)
            print("Deleting textbooks with ISBN: " + ISBN)
            queryset.delete()
            return queryset
        except:
            print("Could not delete textbooks with ISBN: " + ISBN)
            pass

    def add_ISBN():
        pass

    def update_ISBN():
        pass

    def update_view_count():
        pass

    def submit_review():
        pass
