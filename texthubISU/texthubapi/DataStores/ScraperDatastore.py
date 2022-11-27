import os
import subprocess
import threading
from ..scraperstuff.scraper import main
# texthubISU\scraperstuff\scraper.py
# C:\Users\firef\Documents\VsCodeStuff\textbookscraper\theProj\TextHubISU\texthubISU\scraperstuff\scraper.py


class ScraperDatastore():
    def PopulateDatabase():
        print("calling the process")
        #os.system("python texthubapi\scraperstuff\scraper.py pleasejustwork")
        example = threading.Thread(target=main)
        example.start()
        example.join()

        #subprocess.run("python scraperstuff\scraper.py")

        #outputString = scrapeAmazonBook('9780446310789')
        # file2.writelines(']')
        # file2.close()
        # file1.close()


"""{"ISBN": "9780357132692", "Author": " ", "BookName": " ", "Price": " ", "Url": "Amazon.com"}"""
