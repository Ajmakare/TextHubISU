from ..DataStores.TextbookDataStore import *
from ..ServiceFiles.TextbookService import *

class TextbookController:
        
    def do_search_controller(ISBN, sort):
        return TextbookDataStore.do_search(ISBN, sort)

    def request_ISBN_controller(ISBN):
        return TextbookService.request_ISBN_service(ISBN)

    def retrieve_all_textBooks_controller():
        return TextbookDataStore.retrieve_all_textBooks()
        # pass

    def delete_ISBN_controller(request):
        return TextbookService.delete_ISBN_service(request)

    def add_ISBN_controller(request):
        return TextbookService.add_ISBN_service(request)

    def update_ISBN_controller(request):
        return TextbookService.update_ISBN_service(request)

    def update_view_count_controller(ISBN):
        return TextbookDataStore.update_view_count(ISBN)
        # pass

    def submit_review_controller(request):
        return TextbookService.submit_review_service(request)
