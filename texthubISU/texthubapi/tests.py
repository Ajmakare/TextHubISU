from sqlite3 import IntegrityError
from django.test import TestCase, RequestFactory, Client
from texthubapi.Controllers.TextbookController import *
from texthubapi.DataStores.TextbookDataStore import *
from texthubapi.DataStores.UserDataStore import *
from texthubapi.ServiceFiles.SiteService import *
from texthubapi.ServiceFiles.UserService import *
from .models import *
from http import HTTPStatus
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from .views import *
from .scraperstuff.scraper import TextbookScraper
from .scraperstuff.scraper import *

class ScraperTest(TestCase): 
    @classmethod
    def setUp(self):
        pass

    def test_smoke_scraper(self):
        self.assertFalse(Textbook.objects.filter(ISBN='9780060935467').exists())
        result = TextbookScraper.scrape_item('9780060935467')
        self.assertTrue(Textbook.objects.filter(ISBN='9780060935467').exists())
    def test_scraper_fake_isbn(self):
        result = TextbookScraper.scrape_item('97800609353467')
        self.assertFalse(Textbook.objects.filter(ISBN='97800609353467').exists())


class SiteDataStoreTest(TestCase):
    @classmethod
    def setUp(self):
        pass

    def test_submit_feedback(self):
        feedback_text = "This is a test feedback"
        feedback = Feedback(feedback_content=feedback_text)
        SiteDatastore.submit_feedback(feedback)
        self.assertTrue(Feedback.objects.filter(feedback_content=feedback_text).exists())

class TextbookDataStoreTest(TestCase):
    @classmethod
    def setUp(self):
        self.textbook = Textbook.objects.create(
            ISBN='testisbn', author='Aidan', name='how to code', view_count=0)

    def test_submit_review_pass(self):
        new_review = Review(review_content="This is a review",
                            ISBN=Textbook.objects.get(pk='testisbn'))
        TextbookDataStore.submit_review(new_review)
        found_review = Review.objects.filter(review_content='This is a review')
        self.assertTrue(found_review)

    def test_submit_review_fail(self):
        notareview = 'I am not a review'
        with self.assertRaises(AttributeError):
            TextbookDataStore.submit_review(notareview)

    def test_do_search_pass(self):
        queryset = TextbookDataStore.do_search('testisbn', 'default')
        self.assertEqual(str(
            queryset), '{\'bookinfos\': <QuerySet [<Textbook: Textbook object (testisbn)>]>, \'sources\': <QuerySet []>}')

    def test_do_search_fail(self):
        queryset = TextbookDataStore.do_search('notindatabase', 'default')
        self.assertEqual(
            str(queryset), '{\'bookinfos\': <QuerySet []>, \'sources\': <QuerySet []>}')

    def test_do_search_sortalphabetically_pass(self):
        queryset = TextbookDataStore.do_search('testisbn', 'alpha')
        self.assertEqual(str(
            queryset), '{\'bookinfos\': <QuerySet [<Textbook: Textbook object (testisbn)>]>, \'sources\': <QuerySet []>}')

    def test_do_search_sortprice_pass(self):
        queryset = TextbookDataStore.do_search('testisbn', 'price')
        self.assertEqual(str(
            queryset), '{\'bookinfos\': <QuerySet [<Textbook: Textbook object (testisbn)>]>, \'sources\': <QuerySet []>}')

    def test_retrieve_all_textBooks(self):
        queryset = "{'bookinfos': <QuerySet [<Textbook: Textbook object (testisbn)>]>}"
        self.assertEqual(
            str(TextbookDataStore.retrieve_all_textBooks()), str(queryset))

    def test_retrieve_all_textBooks_empty_database(self):
        Textbook.objects.all().delete()
        queryset = "{'bookinfos': <QuerySet []>}"
        self.assertEqual(
            str(TextbookDataStore.retrieve_all_textBooks()), str(queryset))

    def test_delete_ISBN(self):
        TextbookDataStore.delete_ISBN("testisbn")
        testbook = Textbook.objects.filter(ISBN="testisbn")
        self.assertFalse(testbook.exists())

    def test_delete_ISBN_not_found(self):
        with self.assertRaises(ValueError):
            TextbookDataStore.delete_ISBN("notindatabase")

    def test_add_ISBN(self):
        new_textbook = Textbook(ISBN = 'newisbn', author = 'Noah', name = 'how to code 2', view_count = 0)
        TextbookDataStore.add_ISBN(new_textbook)
        self.assertTrue(Textbook.objects.filter(ISBN = 'newisbn').exists())

    # adding book that's already in database
    def test_add_ISBN_fail(self):
        newtestbook = Textbook(ISBN = 'testisbn', author = 'Aidan', name = 'how to code', view_count = 0)
        with self.assertRaises(AttributeError):
            TextbookDataStore.add_ISBN(newtestbook)

    def test_update_view_count(self):
        TextbookDataStore.update_view_count("testisbn")
        testbook = Textbook.objects.get(ISBN="testisbn")
        self.assertEqual(testbook.view_count, 1)

    def test_update_ISBN_pass(self):
        old_textbook = Textbook.objects.filter(ISBN='testisbn')
        updated_textbook = Textbook.objects.get(pk='testisbn')
        updated_textbook.name = 'new name'
        updated_textbook.author = 'new author'
        TextbookDataStore.update_ISBN(updated_textbook)
        self.assertNotEqual(old_textbook, Textbook.objects.get(pk='testisbn'))

    def test_update_ISBN_fail(self):
        notatextbook = 'I am not a textbook'
        with self.assertRaises(AttributeError):
            TextbookDataStore.update_ISBN(notatextbook)
    
    def test_request_ISBN_pass(self):
        testISBN = '9783029321382'
        testRequest = Request(requestISBN= testISBN)
        TextbookDataStore.request_ISBN(testRequest)
        testQuery = Request.objects.filter(requestISBN= testISBN)
        self.assertTrue(testQuery.exists())

    def test_request_ISBN_fail(self):
        notarequest = 'Invalid Request'
        with self.assertRaises(AttributeError):
            TextbookDataStore.request_ISBN(notarequest)


class UserDataStoreTest(TestCase):
    @classmethod
    def setUp(self):
        self.currentUser = User.objects.create_user(
            username='testusername',
            email='testemail@gmail.com',
            password='testpassword')

    def test_add_user_pass(self):
        UserDataStore.add_user('testnewusername', 'testnewemail@gmail.com', 'testnewpassword')
        login = self.client.login(username='testnewusername', password='testnewpassword')
        self.assertTrue(login)

    def test_add_user_fail(self):
        with self.assertRaises(AttributeError):
            UserDataStore.add_user('testusername', 'testemail@gmail.com', 'testpassword')

class scraperTest(TestCase):
    def setUp(self):
        pass

    def test_obtainISBNs_pass(self):
        file = open("texthubapi/TestingFiles/ISUISBNs_validtesting.txt", "r")
        currentList = TextbookScraper.obtainISBNs()

        Validlist = []
        for line in file:
            stripped_line = line.strip()
            Validlist.append(stripped_line)

        self.assertTrue(len(currentList)==len(Validlist))

class SiteServiceTest(TestCase):
    @classmethod
    def setUp(self):
        pass

    def test_submit_feedback(self):
        request = RequestFactory().post(
            '/home', data={'FeedbackContent': 'testfeedback'})
        SiteService.submit_feedback_service(request)
        testfeedback = Feedback.objects.filter(feedback_content="testfeedback")
        self.assertTrue(testfeedback.exists())


class TextbookServiceTest(TestCase):
    @classmethod
    def setUp(self):
        self.textbook = Textbook.objects.create(
            ISBN='testisbn', author='Aidan', name='how to code', view_count=0)

    def test_update_ISBN_pass(self):
        old_book = Textbook.objects.filter(ISBN='testisbn')
        request = RequestFactory().post('/admin2',
                                        data={'ISBNToUpdate': 'testisbn', 'name': 'new name', 'author': 'new author'})
        TextbookService.update_ISBN_service(request)
        updated_book = Textbook.objects.filter(ISBN='testisbn')
        self.assertNotEqual(old_book, updated_book)

    def test_update_ISBN_fail(self):
        notatextbook = 'I am not a textbook'
        with self.assertRaises(AttributeError):
            TextbookService.update_ISBN_service(notatextbook)

    def test_review_pass(self):
        request = RequestFactory().post(
            '/home', data={'ISBNToReview': 'testisbn', 'ReviewContent': 'This book is awesome!'})
        TextbookService.submit_review_service(request)
        review = Review.objects.filter(review_content='This book is awesome!')
        self.assertTrue(review.exists())

    def test_review_fail(self):
        notareview = 'I am not a review'
        with self.assertRaises(AttributeError):
            TextbookService.update_ISBN_service(notareview)

    def test_retrieve_all_textBooks_service(self):
        queryset = "{'bookinfos': <QuerySet [<Textbook: Textbook object (testisbn)>]>}"
        self.assertEqual(
            str(TextbookService.retrieve_all_textbooks_service()), str(queryset))

    def test_delete_ISBN_service(self):
        request = RequestFactory().post(
            '/deleteisbn', data={'ISBNToDelete': 'testisbn'})
        TextbookService.delete_ISBN_service(request)
        testbook = Textbook.objects.filter(ISBN="testisbn")
        self.assertFalse(testbook.exists())

    def test_delete_ISBN_service_not_found(self):
        request = RequestFactory().post(
            '/deleteisbn', data={'ISBNToDelete': 'notindatabase'})
        with self.assertRaises(ValueError):
            TextbookService.delete_ISBN_service(request)

    def test_request_isbn_service_pass(self):
        request = RequestFactory().post('/home', data={'ISBN' : 'testrequest'})
        ISBN_to_request = request.POST
        TextbookService.request_ISBN_service(ISBN_to_request)
        testRequest = Request.objects.filter(requestISBN="testrequest")
        self.assertTrue(testRequest.exists())

class UserServiceTest(TestCase):
    @classmethod
    def setUp(self):
        user = User.objects.create_user(username='admin', password='admin', email="johnwhite@gmail.com")
        pass

    def add_user_service_pass(self):
        testrequest = RequestFactory().post('/admin', data={'Email': 'testEmail@gmail.com',
            'Username':'testUsername', 'Password': 'testPassword'})
        UserService.add_user_service(testrequest)
        login = self.client.login(username='testUsername', password='testPassword')
        self.assertTrue(login)

    def add_user_service_invalidform(self):
        testrequest = RequestFactory().post('/admin', data={'Email': 'testIncorrectEmailFormat',
            'Username':'testUsername', 'Password': 'testPassword'})
        self.assertTrue(UserService.add_user_service(testrequest) == "Form Invalid")

    def add_user_service_duplicate_username(self):
        self.initialUser = User.objects.create_user(
            username='testusername',
            email='testemail@gmail.com',
            password='testpassword')
        testrequest = RequestFactory().post('/admin', data={
            'Email': 'othertestemail@gmail.com',
            'Username':'testusername', 
            'Password': 'othertestpassword'})
        self.assertTrue(UserService.add_user_service(testrequest) == "Duplicate username or email already exists")

    def add_user_service_duplicate_email(self):
        self.initialUser = User.objects.create_user(
            username='testusername',
            email='testemail@gmail.com',
            password='testpassword')
        testrequest = RequestFactory().post('/admin', data={
            'Email': 'testemail@gmail.com',
            'Username':'othertestusername', 
            'Password': 'othertestpassword'})
        self.assertTrue(UserService.add_user_service(testrequest) == "Duplicate username or email already exists")
    
    def test_user_login(self):
        c = Client()
        response = c.post('/login2', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 301)

class ViewsTest(TestCase):
    @classmethod
    def setUp(self):
        self.textbook = Textbook.objects.create(
            ISBN='testisbn', author='Aidan', name='how to code', view_count=0)
        pass

    def test_home_submit_feedback_view(self):
        self.client.post('/home', data={'FeedbackContent': 'feedbacktimewoo'})
        self.assertTrue(Feedback.objects.filter(
            feedback_content='feedbacktimewoo').exists())

    def test_admin_delete_ISBN_view(self):
        self.client.post('/admin2/', data={'ISBNToDelete': 'testisbn'})
        textbook = Textbook.objects.filter(ISBN='testisbn')
        self.assertFalse(textbook.exists())

    def test_admin_delete_ISBN_view_not_found(self):
        response = self.client.post(
            '/admin2/', data={'ISBNToDelete': 'notindatabase'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         "Could not delete ISBN from database!")

    def test_admin_update_ISBN_view(self):
        old_book = Textbook.objects.filter(ISBN='testisbn')
        self.client.post(
            '/admin2/', data={'ISBNToUpdate': 'testisbn', 'name': 'new name', 'author': 'new author'})
        updated_book = Textbook.objects.filter(ISBN='testisbn')
        self.assertNotEqual(old_book, updated_book)

    def test_admin_update_ISBN_view_not_found(self):
        response = self.client.post(
            '/admin2/', data={'ISBNToUpdate': 'notindatabase', 'name': 'new name', 'author': 'new author'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "ISBN not in database!")

    def test_home_search_ISBN_pass(self):
        response = self.client.post('/home', data={'ISBN': 'testisbn'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_home_search_ISBN_both_sorts_fail(self):
        response = self.client.post(
            '/home', data={'ISBN': 'testisbn', 'SortAlphabetical': 'True', 'SortByPrice': 'True'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Please select only 1 sort method")

    def test_home_search_ISBN_sort_alphabetical(self):
        response = self.client.post(
            '/home', data={'ISBN': 'testisbn', 'SortAlphabetical': 'True'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_home_search_ISBN_sort_by_price(self):
        response = self.client.post(
            '/home', data={'ISBN': 'testisbn', 'SortByPrice': 'True'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_home_search_isbn_doesnotexist(self):
        response = self.client.post('/home', data = {'ISBN':'notindatabase'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_home_request_isbn_redirect(self):
        response = self.client.post('/home', data = {'ISBN':'nonexistentisbn'})
        self.assertRedirects(response,'/sendrequest/')

    def test_send_request_pass(self):
        self.client.post('/home', data={'ISBN': 'testrequestisbn'}, follow=True)
        request = RequestFactory().post('/sendRequest', data={'RequestButton': True})
        request.session = {}
        Views.sendRequest_view(request)
        #session = 
        testNewRequest = Request.objects.filter(requestISBN='testrequestisbn')
        self.assertFalse(testNewRequest.exists())
        

