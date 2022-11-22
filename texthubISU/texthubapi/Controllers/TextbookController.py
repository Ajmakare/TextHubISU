from ..DataStores.TextbookDataStore import *

class TextbookController:
        
    def do_search_controller(ISBN):
            return TextbookDataStore.do_search(ISBN)

    def request_ISBN_controller():
        pass

    def retrieve_all_textBooks_controller():
        pass

    def delete_ISBN_controller(request):
        return TextbookDataStore.delete_ISBN(request)

    def add_ISBN_controller(request):
        return TextbookDataStore.add_ISBN(request)

    def update_ISBN_controller(request):
        return TextbookDataStore.update_ISBN(request)

    def update_view_count_controller():
        pass

    def submit_review_controller(request):
        return TextbookDataStore.submit_review(request)
