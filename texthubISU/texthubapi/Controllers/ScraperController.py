from ..DataStores.TextbookDataStore import *
import threading
from ..scraperstuff.scraper import main


class ScraperController:
    def scrape_controller():
        example = threading.Thread(target=main)
        example.start()
        example.join()
