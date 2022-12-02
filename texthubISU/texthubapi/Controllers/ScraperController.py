from ..DataStores.TextbookDataStore import *


class ScraperController:
    def scrape_controller():
        print('calling populate db datastore')
        return TextbookDataStore.populate_db()
