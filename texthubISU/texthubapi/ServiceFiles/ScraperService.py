from ..scraperstuff.scraper import main
import threading
class ScraperService():
    
   def scraper_service():
        example = threading.Thread(target=main)
        example.start()
        example.join()