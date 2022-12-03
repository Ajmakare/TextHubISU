from ..DataStores.TextbookDataStore import *
import threading
from ..scraperstuff.scraper import main
from ..ServiceFiles.ScraperService import *


class ScraperController:
    def scrape_controller():
        return ScraperService.scraper_service()
