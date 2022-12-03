from django.http import HttpResponse
from django.shortcuts import render
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import sys
from ..models import *
from abc import ABC
from selenium.webdriver.chrome.options import Options
import json
from itertools import chain
from texthubapi.DataStores.TextbookDataStore import TextbookDataStore
import os
import PyPDF2


service = Service(executable_path="texthubapi/scraperstuff/chromedriver.exe")
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.


class Scraper(ABC):  # the abstracgt class
    def scrapeItem():
        pass

    def obtain_ISBNs():
        pass


class TextbookScraper(Scraper):
    def scrape_item(isbn):
        price = " "
        author = " "
        bookName = " "
        # put chrome_options = options next to service param to make it headless :D
        # chrome_options=options
        textbook = [isbn, author, bookName, price, 'Amazon.com']
        print("attempting to run the scraper")
        driver = webdriver.Chrome(service=service)
        driver.get("https://www.amazon.com")

        driver.implicitly_wait(1.5)
        try:
            text_box = driver.find_element(
                by=By.CSS_SELECTOR, value='input[id="twotabsearchtextbox"]')
        except Exception as e:
            print('could not find the search bar lol')
            jsonpart = json.dumps(textbook)
            return jsonpart
        try:
            submit_button = driver.find_element(
                by=By.CSS_SELECTOR, value='input[id="nav-search-submit-button"]')
        except Exception as e:
            print('search button not loadingh')
            jsonpart = json.dumps(textbook)
            return jsonpart

        text_box.send_keys(isbn)
        submit_button.click()
        try:
            priceElement = driver.find_element(
                by=By.CSS_SELECTOR, value='span[class="a-price-whole"]')
            price = str(priceElement.text)
            print(price)

        except Exception as e:
            print('error price')
        try:
            authorElement = driver.find_element(
                by=By.CSS_SELECTOR, value='a[class="a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style"]')

            # <a class="a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style" href="/Harper-Lee/e/B00456LE3M?ref=sr_ntt_srch_lnk_1&amp;qid=1670095092&amp;sr=1-1">Harper Lee</a>
            # authorElement = driver.find_element(
            #     By.XPATH, '//span[text()="by "]')
            author = str(authorElement.text)

        except Exception as e:
            print('error author')
        try:
            bookNameElement = driver.find_element(
                by=By.CSS_SELECTOR, value='span[class="a-size-medium a-color-base a-text-normal"]')
            bookName = str(bookNameElement.text)

        except Exception as e:
            print('error bookname')

        print(textbook)
        textbook = [isbn, author, bookName, price, 'Amazon.com']

        if textbook[0] != None and textbook[3] != ' ':

            new_textbook = Textbook()
            new_textbook.ISBN = textbook[0]
            new_textbook.author = textbook[1]
            new_textbook.name = textbook[2]
            price1 = float(textbook[3])
            new_textbook.view_count = 0
            new_source = Source(
                price=price1, url=textbook[4], ISBN=new_textbook)
            TextbookDataStore.add_ISBN(new_textbook)
            TextbookDataStore.add_source(new_source, 'Amazon.com')
            Textbook
            print('about to save a mf textbookzz')
            print(new_textbook.name)
        # print (jsonpart)
        driver.quit()

        # message = driver.find_element(by=By.ID, value="message")
        # value = message.text
        # assert value == "Received!"
    def obtainISBNs():
        # reading the pdf in a binary mode "rb"
        inputFile = open('texthubapi/scraperstuff/isutextbookspdf.pdf', 'rb')
        reader = PyPDF2.PdfFileReader(inputFile)
        listOfISBNs = []
        repeatedWords = list()
        for i in range(reader.numPages):
            currentPage = reader.getPage(i)
            text = currentPage.extract_text()
            words = text.split(' ')

            for j in range(len(words)):
                # removing all hyphens before collecting isbn substring
                curISBN = words[j].replace('-', '')
                curIndex = curISBN.find("978")
                curISBN = curISBN[curIndex:curIndex+13]
                if (curIndex != -1 and not repeatedWords.__contains__(curISBN)):
                    repeatedWords.append(curISBN)
                    listOfISBNs.append(curISBN+"\n")

        inputFile.close()
        return listOfISBNs


def main():
    # if sys.argv[1] == 'pleasejustwork':

    isbns = TextbookScraper.obtainISBNs()
    count = 0

    # Strips the newline character
    # file2 = open('output.json', 'w')
    # file2.writelines('[')
    for line in isbns:
        count += 1

        output = TextbookScraper.scrape_item(line.strip())
        print(output)
