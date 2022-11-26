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

    def test_submit_review_pass(self):
        response = self.client.post('/home', data = {'ISBNToReview': 'testisbn','ReviewContent':'12020424' })
        self.assertEqual(response.status_code, HTTPStatus.OK)

