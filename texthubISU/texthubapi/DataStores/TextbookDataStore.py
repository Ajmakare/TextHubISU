from ..serializers import *
from ..models import Textbook

class TextbookDataStore():
    # Get all data (rows) associated with an ISBN
    # We want to retrieve all site info for a single isbn to display to user
    def do_search(ISBN):
        try:
            queryset = Textbook.objects.raw('select texthubapi_textbook.ISBN as \'textbook_ISBN\', texthubapi_textbook.author, texthubapi_textbook.name, texthubapi_textbook.view_count, texthubapi_source.price, texthubapi_source.url, texthubapi_source.ISBN from texthubapi_textbook inner join texthubapi_source on textbook_ISBN = texthubapi_source.ISBN')
            return queryset
        except:
            print("Could not retrieve textbooks with ISBN: " + ISBN)
            pass

    def request_ISBN():
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
