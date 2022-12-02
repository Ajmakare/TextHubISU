from django.test import TestCase,RequestFactory
from texthubapi.Controllers.TextbookController import *
from texthubapi.DataStores.TextbookDataStore import *
from .models import *
from http import HTTPStatus
from django.contrib.messages import get_messages

class UserDatastoreTest(TestCase):
    @classmethod
    def setUp(self):
        testUser = User.objects.create_user('user', 'email', 'Password')

    def test_add_user_pass(self):
        


# Note for others making tests - Tests create a seperate database from our app! So set up what you need.
class TextbookTest(TestCase):
    @classmethod
    def setUp(self):
        # Textbook object for review object (isbn is foreign key for Review object)
        self.textbook = Textbook.objects.create(ISBN = 'testisbn', author = 'Aidan', name = 'how to code', view_count = 0)
        # self.feedback = Feedback.objects.create(feedback_content = 'feedback')

    # Test search ISBN with default sort (by ID)
    def test_search_isbn_pass(self):
        response = self.client.get('/textbooks/testisbn/default')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test search ISBN with isbn not in database (redirects to request page code 302=FOUND)
    def test_search_isbn_fail(self):
        response = self.client.post('/home', data = {'ISBN': 'notindatabase','SortAlphabetical': False, 'SortByPrice': False})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    # Test search ISBN with sort my alphabetical param
    def test_search_isbn_pass_alpha(self):
        response = self.client.get('/textbooks/testisbn/alpha')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test search ISBN with sort by price param
    def test_search_isbn_pass_price(self):
        response = self.client.get('/textbooks/testisbn/price')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test retrieve all textbooks
    def test_retrieve_all_textbooks_pass(self):
        response = self.client.get('/retrieve')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test delete ISBN
    def test_delete_ISBN_pass(self):
        self.client.post('/admin2', data = {'ISBNToDelete': 'testisbn'})
        textbook = Textbook.objects.filter(ISBN = 'testisbn')
        self.assertFalse(textbook.exists())

    # Test delete ISBN with ISBN not in database
    def test_delete_ISBN_fail(self):
        with self.assertRaises(ValueError):
            TextbookDataStore.delete_ISBN('notindatabase')

    # Test submit review success (POST)
    def test_submit_review_pass(self):
        self.client.post('/home', data = {'ISBNToReview': 'testisbn','ReviewContent':'12020424' })
        review = Review.objects.filter(review_content = '12020424')
        self.assertTrue(review.exists())

    # Test submit review fail (POST) - ISBN not in DB
    def test_submit_review_fail(self):
        response = self.client.post('/home', data = {'ISBNToReview': 'notindatabase','ReviewContent':'12020424'})
        review = Review.objects.filter(review_content = '12020424')
        self.assertFalse(review.exists())

    # Test submitting site feedback
    def test_submit_feedback_pass(self):
        self.client.post('/home', data = {'FeedbackContent': 'newfeedback'})
        feedback = Feedback.objects.filter(feedback_content = 'newfeedback')
        self.assertTrue(feedback.exists())

    # Test submitting site feedback with no content
    def test_submit_feedback_fail(self):
        self.client.post('/home', data = {'FeedbackContent': ''})
        feedback = Feedback.objects.filter(feedback_content = '')
        self.assertFalse(feedback.exists())

    # Test update a textbook in database
    def test_update_ISBN_pass(self):
        old_textbook = Textbook.objects.filter(ISBN = 'testisbn')
        self.client.post('/admin2', data = {'ISBNToUpdate': 'testisbn','name':'new name', 'author': 'new author'})
        new_textbook = Textbook.objects.filter(ISBN = 'testisbn')
        self.assertNotEqual(old_textbook, new_textbook) 

    # Test update a textbook in database fail
    def test_update_ISBN_fail(self):
        response = self.client.post('/admin2', data = {'ISBNToUpdate': 'notindatabase','name':'new name', 'author': 'new author'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'ISBN not in database!')

    # Test requesting an ISBN after searching an invalid ISBN
    def test_request_ISBN_pass(self):
        response = self.client.post('/home', data = {'ISBN': 'testrequestisbn','SortAlphabetical': False, 'SortByPrice': False}, follow=True)
        self.assertRedirects(response, '/sendrequest')
        self.client.post('/sendrequest', data = {'RequestButton': True})
        requestedISBN = Request.objects.filter(requestISBN = 'testrequestisbn')
        self.assertTrue(requestedISBN.exists())

    def test_request_ISBN_noredirect(self):
        response = self.client.post('/home', data = {'ISBN': 'testisbn','SortAlphabetical': False, 'SortByPrice': False}, follow=True)
        not self.assertRedirects(response, '/sendrequest')
        RequestedISBN = Request.objects.filter(requestISBN = '')
        self.assertFalse(RequestedISBN.exists())