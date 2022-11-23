from django.http import HttpResponse
from django.shortcuts import render
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import sys
from ..models import Textbook
from abc import ABC
from selenium.webdriver.chrome.options import Options
import json
from itertools import chain
import os


service = Service(executable_path="texthubapi/scraperstuff/chromedriver.exe")
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.

# class Scraper(ABC):  # the abstracgt class
#     def scrapeItem(self):
#         pass


class ScrapeTextbook:
    def scrapeItem(isbn):
        price = " "
        author = " "
        bookName = " "
        textbook = [isbn, author, bookName, price, 'Amazon.com']
        # put chrome_options = options next to service param to make it headless :D
        # chrome_options=options
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

        except Exception as e:
            print('error price')
        try:
            # authorElement = driver.find_element(
            #     by=By.CSS_SELECTOR, value='span[class="div.a-row"]')
            authorElement = driver.find_element(
                By.XPATH, '//span[text()="by "]')
            author = str(authorElement.text)

        except Exception as e:
            print('error author')
        try:
            bookNameElement = driver.find_element(
                by=By.CSS_SELECTOR, value='span[class="a-size-medium a-color-base a-text-normal"]')
            bookName = str(bookNameElement.text)

        except Exception as e:
            print('error bookname')

        if textbook[0] != None:

            new_textbook = Textbook()
            new_textbook.ISBN = textbook[0]
            new_textbook.author = textbook[1]
            new_textbook.name = textbook[2]
            new_textbook.view_count = 0
            print('about to save a mf textbookzz')
            print (new_textbook.name)
            new_textbook.save()
        # print (jsonpart)
        driver.quit()

        # message = driver.find_element(by=By.ID, value="message")
        # value = message.text
        # assert value == "Received!"


def main():
    # if sys.argv[1] == 'pleasejustwork':

    file1 = open('texthubapi/scraperstuff/isbns.txt', 'r')
    Lines = file1.readlines()
    count = 0

    # Strips the newline character
    # file2 = open('output.json', 'w')
    # file2.writelines('[')
    for line in Lines:
        count += 1

        output = ScrapeTextbook.scrapeItem(line.strip())
        print(output)
