from ..DataStores.TextbookDataStore import *

def do_search_controller(ISBN):
    try:
        return TextbookDataStore.do_search(ISBN)
    except:
        pass

def request_ISBN_controller():
    pass

def retrieve_all_textBooks_controller():
    pass

def delete_ISBN_controller():
    pass

def add_ISBN_controller():
    pass

def update_ISBN_controller():
    pass

def update_view_count_controller():
    pass
