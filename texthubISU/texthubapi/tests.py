from django.test import TestCase,RequestFactory
from texthubapi.Controllers.TextbookController import *
from texthubapi.DataStores.TextbookDataStore import *
from .models import *
from http import HTTPStatus

class AdminTest(TestCase):
    pass

class TextbookTest(TestCase):
    @classmethod
    def setUp(self):
        # Textbook object for review object (isbn is foreign key for Review object)
        self.textbook = Textbook.objects.create(ISBN = 'testisbn', author = 'Aidan', name = 'how to code', view_count = 0)

    # Test submit valid review (POST)
    def test_submit_review_pass(self):
        response = self.client.post('/home', data = {'ISBNToReview': 'testisbn','ReviewContent':'12020424' })
        review = Review.objects.filter(review_content = '12020424')
        self.assertTrue(review.exists())

    # Test update a textbook in database
    def test_update_ISBN_pass(self):
        old_textbook = Textbook.objects.filter(ISBN = 'testisbn')
        self.client.post('/admin2', data = {'ISBNToUpdate': 'testisbn','name':'new name', 'author': 'new author'})
        new_textbook = Textbook.objects.filter(ISBN = 'testisbn')
        self.assertNotEqual(old_textbook, new_textbook) 
    
    # Test search ISBN with default sort (by ID)
    def test_search_isbn_pass(self):
        response = self.client.get('/textbooks/testisbn/default')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test search ISBN with sort my alphabetical param
    def test_search_isbn_pass_alpha(self):
        response = self.client.get('/textbooks/testisbn/alpha')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test search ISBN with sort by price param
    def test_search_isbn_pass_price(self):
        response = self.client.get('/textbooks/testisbn/price')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test search ISBN with isbn not in database (redirects to request page code 302=FOUND)
    def test_search_isbn_fail(self):
        response = self.client.post('/home', data = {'ISBN': 'notindatabase','SortAlphabetical': False, 'SortByPrice': False})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
