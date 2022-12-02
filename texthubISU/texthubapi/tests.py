from django.test import TestCase, RequestFactory
from texthubapi.Controllers.TextbookController import *
from texthubapi.DataStores.TextbookDataStore import *
from texthubapi.DataStores.UserDataStore import *
from texthubapi.ServiceFiles.SiteService import *
from .models import *
from http import HTTPStatus
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model

# Import stuff accordingly
class ScraperDataStoreTest(TestCase):
    @classmethod
    def setUp(self):
        pass

class SiteDataStoreTest(TestCase):
    @classmethod
    def setUp(self):
        pass

class TextbookDataStoreTest(TestCase):
    @classmethod
    def setUp(self):
        self.textbook = Textbook.objects.create(ISBN = 'testisbn', author = 'Aidan', name = 'how to code', view_count = 0)

    def test_submit_review_pass(self):
        new_review = Review(review_content="This is a review", ISBN = Textbook.objects.get(pk = 'testisbn'))
        TextbookDataStore.submit_review(new_review)
        found_review = Review.objects.filter(review_content = 'This is a review')
        self.assertTrue(found_review)

    def test_submit_review_fail(self):
        notareview = 'I am not a review'
        with self.assertRaises(AttributeError):
            TextbookDataStore.submit_review(notareview)

    def test_do_search_pass(self):
        queryset = TextbookDataStore.do_search('testisbn', 'default')
        self.assertEqual(str(queryset), '{\'bookinfos\': <QuerySet [<Textbook: Textbook object (testisbn)>]>, \'sources\': <QuerySet []>}')

    def test_do_search_fail(self):
        queryset = TextbookDataStore.do_search('notindatabase', 'default')
        self.assertEqual(str(queryset), '{\'bookinfos\': <QuerySet []>, \'sources\': <QuerySet []>}')

    def test_do_search_sortalphabetically_pass(self):
        queryset = TextbookDataStore.do_search('testisbn', 'alpha')
        self.assertEqual(str(queryset), '{\'bookinfos\': <QuerySet [<Textbook: Textbook object (testisbn)>]>, \'sources\': <QuerySet []>}')
    
    def test_do_search_sortprice_pass(self):
        queryset = TextbookDataStore.do_search('testisbn', 'price')
        self.assertEqual(str(queryset), '{\'bookinfos\': <QuerySet [<Textbook: Textbook object (testisbn)>]>, \'sources\': <QuerySet []>}')

    def test_retrieve_all_textBooks(self):
        queryset = "{'bookinfos': <QuerySet [<Textbook: Textbook object (testisbn)>]>}"
        self.assertEqual(str(TextbookDataStore.retrieve_all_textBooks()), str(queryset))

    def test_retrieve_all_textBooks_empty_database(self):
        Textbook.objects.all().delete()
        queryset = "{'bookinfos': <QuerySet []>}"
        self.assertEqual(str(TextbookDataStore.retrieve_all_textBooks()), str(queryset))

    def test_delete_ISBN(self):
        TextbookDataStore.delete_ISBN("testisbn")
        testbook = Textbook.objects.filter(ISBN="testisbn")
        self.assertFalse(testbook.exists())

    def test_delete_ISBN_not_found(self):
        with self.assertRaises(ValueError):
            TextbookDataStore.delete_ISBN("notindatabase")

    def test_update_view_count(self):
        TextbookDataStore.update_view_count("testisbn")
        testbook = Textbook.objects.get(ISBN="testisbn")
        self.assertEqual(testbook.view_count, 1)
        
    def test_update_ISBN_pass(self):
        old_textbook = Textbook.objects.filter(ISBN = 'testisbn')
        updated_textbook = Textbook.objects.get(pk='testisbn')
        updated_textbook.name = 'new name'
        updated_textbook.author = 'new author'
        TextbookDataStore.update_ISBN(updated_textbook)
        self.assertNotEqual(old_textbook, Textbook.objects.get(pk='testisbn')) 
          
    def test_update_ISBN_fail(self):
        notatextbook = 'I am not a textbook'
        with self.assertRaises(AttributeError):
            TextbookDataStore.update_ISBN(notatextbook)

        
class UserDataStoreTest(TestCase):
    @classmethod
    def setUp(self):
        self.currentUser = User.objects.create_user(
            username='testusername',
            email='testemail',
            password='testpassword')

    def test_add_user_pass(self):
        UserDataStore.add_user('testnewusername', 'testnewemail', 'testnewpassword')
        login = self.client.login(username='testnewusername', password='testnewpassword')
        self.assertTrue(login)

    def test_add_user_fail(self):
        with self.assertRaises(AttributeError):
            UserDataStore.add_user('testusername', 'testemail', 'testpassword')


class SiteServiceTest(TestCase):
    @classmethod
    def setUp(self):
        pass

    def test_submit_feedback(self):
        request = RequestFactory().post('/home', data={'FeedbackContent': 'testfeedback'})
        SiteService.submit_feedback_service(request)
        testfeedback = Feedback.objects.filter(feedback_content="testfeedback")
        self.assertTrue(testfeedback.exists())

class TextbookServiceTest(TestCase):
    @classmethod
    def setUp(self):
        self.textbook = Textbook.objects.create(ISBN = 'testisbn', author = 'Aidan', name = 'how to code', view_count = 0)
    
    def test_update_ISBN_pass(self):
        old_book = Textbook.objects.filter(ISBN = 'testisbn')
        request = RequestFactory().post('/admin2', data={'ISBNToUpdate': 'testisbn', 'name':'new name', 'author':'new author'})
        TextbookService.update_ISBN_service(request)
        updated_book = Textbook.objects.filter(ISBN = 'testisbn')
        self.assertNotEqual(old_book, updated_book)    
        
    def test_update_ISBN_fail(self):
        notatextbook = 'I am not a textbook'
        with self.assertRaises(AttributeError):
            TextbookService.update_ISBN_service(notatextbook)
            
    def test_review_pass(self):
        request = RequestFactory().post('/home', data={'ISBNToReview': 'testisbn', 'ReviewContent':'This book is awesome!'})
        TextbookService.submit_review_service(request)
        review = Review.objects.filter(review_content = 'This book is awesome!')
        self.assertTrue(review.exists())
        
    def test_review_fail(self):
        notareview = 'I am not a review'
        with self.assertRaises(AttributeError):
            TextbookService.update_ISBN_service(notareview)

    def test_retrieve_all_textBooks_service(self):
        queryset = "{'bookinfos': <QuerySet [<Textbook: Textbook object (testisbn)>]>}"
        self.assertEqual(str(TextbookService.retrieve_all_textbooks_service()), str(queryset))

    def test_delete_ISBN_service(self):
        request = RequestFactory().post('/deleteisbn', data={'ISBNToDelete': 'testisbn'})
        TextbookService.delete_ISBN_service(request)
        testbook = Textbook.objects.filter(ISBN="testisbn")
        self.assertFalse(testbook.exists())

    def test_delete_ISBN_service_not_found(self):
        request = RequestFactory().post('/deleteisbn', data={'ISBNToDelete': 'notindatabase'})
        with self.assertRaises(ValueError):
            TextbookService.delete_ISBN_service(request)

class UserServiceTest(TestCase):
    @classmethod
    def setUp(self):
        pass

class ViewsTest(TestCase):
    @classmethod
    def setUp(self):
        self.textbook = Textbook.objects.create(ISBN = 'testisbn', author = 'Aidan', name = 'how to code', view_count = 0)
        pass

    def test_home_submit_feedback_view(self):
        self.client.post('/home', data = {'FeedbackContent': 'feedbacktimewoo'})
        self.assertTrue(Feedback.objects.filter(feedback_content = 'feedbacktimewoo').exists())

    def test_admin_delete_ISBN_view(self):
        self.client.post('/admin2/', data = {'ISBNToDelete': 'testisbn'})
        textbook = Textbook.objects.filter(ISBN = 'testisbn')
        self.assertFalse(textbook.exists())

    def test_admin_delete_ISBN_view_not_found(self):
        response = self.client.post('/admin2/', data = {'ISBNToDelete': 'notindatabase'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Could not delete ISBN from database!")    
        
        
    def test_admin_update_ISBN_view(self):
        old_book = Textbook.objects.filter(ISBN = 'testisbn')
        self.client.post('/admin2/', data = {'ISBNToUpdate': 'testisbn', 'name': 'new name', 'author': 'new author'})
        updated_book = Textbook.objects.filter(ISBN = 'testisbn')
        self.assertNotEqual(old_book, updated_book)
        
    def test_admin_update_ISBN_view_not_found(self):
        response = self.client.post('/admin2/', data = {'ISBNToUpdate': 'notindatabase', 'name': 'new name', 'author': 'new author'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "ISBN not in database!")
        
    def test_home_search_ISBN_pass(self):
        response = self.client.post('/home', data = {'ISBN':'testisbn'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)    
    
    def test_home_search_ISBN_both_sorts_fail(self):
        response = self.client.post('/home', data = {'ISBN':'testisbn', 'SortAlphabetical':'True','SortByPrice':'True'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Please select only 1 sort method")
    
    def test_home_search_ISBN_sort_alphabetical(self):
        response = self.client.post('/home', data = {'ISBN':'testisbn', 'SortAlphabetical':'True'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)     
    
    def test_home_search_ISBN_sort_by_price(self):
        response = self.client.post('/home', data = {'ISBN':'testisbn', 'SortByPrice':'True'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)    
    
    def test_home_search_isbn_doesnotexist(self):
        response = self.client.post('/home', data = {'ISBN':'notindatabase'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)    



# # Note for others making tests - Tests create a seperate database from our app! So set up what you need.
# class TextbookTest(TestCase):
#     @classmethod
#     def setUp(self):
#         # Textbook object for review object (isbn is foreign key for Review object)
#         self.textbook = Textbook.objects.create(ISBN = 'testisbn', author = 'Aidan', name = 'how to code', view_count = 0)
#         # self.feedback = Feedback.objects.create(feedback_content = 'feedback')

#     # Test search ISBN with default sort (by ID)
#     def test_search_isbn_pass(self):
#         response = self.client.get('/textbooks/testisbn/default')
#         self.assertEqual(response.status_code, HTTPStatus.OK)

#     # Test search ISBN with isbn not in database (redirects to request page code 302=FOUND)
#     def test_search_isbn_fail(self):
#         response = self.client.post('/home', data = {'ISBN': 'notindatabase','SortAlphabetical': False, 'SortByPrice': False})
#         self.assertEqual(response.status_code, HTTPStatus.FOUND)

#     # Test search ISBN with sort my alphabetical param
#     def test_search_isbn_pass_alpha(self):
#         response = self.client.get('/textbooks/testisbn/alpha')
#         self.assertEqual(response.status_code, HTTPStatus.OK)

#     # Test search ISBN with sort by price param
#     def test_search_isbn_pass_price(self):
#         response = self.client.get('/textbooks/testisbn/price')
#         self.assertEqual(response.status_code, HTTPStatus.OK)

#     # Test retrieve all textbooks
#     def test_retrieve_all_textbooks_pass(self):
#         response = self.client.get('/retrieve')
#         self.assertEqual(response.status_code, HTTPStatus.OK)

#     # Test delete ISBN
#     def test_delete_ISBN_pass(self):
#         self.client.post('/admin2', data = {'ISBNToDelete': 'testisbn'})
#         textbook = Textbook.objects.filter(ISBN = 'testisbn')
#         self.assertFalse(textbook.exists())

#     # Test delete ISBN with ISBN not in database
#     def test_delete_ISBN_fail(self):
#         with self.assertRaises(ValueError):
#             TextbookDataStore.delete_ISBN('notindatabase')

#     # Test submit review success (POST)
#     def test_submit_review_pass(self):
#         self.client.post('/home', data = {'ISBNToReview': 'testisbn','ReviewContent':'12020424' })
#         review = Review.objects.filter(review_content = '12020424')
#         self.assertTrue(review.exists())

#     # Test submit review fail (POST) - ISBN not in DB
#     def test_submit_review_fail(self):
#         response = self.client.post('/home', data = {'ISBNToReview': 'notindatabase','ReviewContent':'12020424'})
#         review = Review.objects.filter(review_content = '12020424')
#         self.assertFalse(review.exists())

#     # Test submitting site feedback
#     def test_submit_feedback_pass(self):
#         self.client.post('/home', data = {'FeedbackContent': 'newfeedback'})
#         feedback = Feedback.objects.filter(feedback_content = 'newfeedback')
#         self.assertTrue(feedback.exists())

#     # Test submitting site feedback with no content
#     def test_submit_feedback_fail(self):
#         self.client.post('/home', data = {'FeedbackContent': ''})
#         feedback = Feedback.objects.filter(feedback_content = '')
#         self.assertFalse(feedback.exists())

#     # Test update a textbook in database
#     def test_update_ISBN_pass(self):
#         old_textbook = Textbook.objects.filter(ISBN = 'testisbn')
#         self.client.post('/admin2', data = {'ISBNToUpdate': 'testisbn','name':'new name', 'author': 'new author'})
#         new_textbook = Textbook.objects.filter(ISBN = 'testisbn')
#         self.assertNotEqual(old_textbook, new_textbook) 

#     # Test update a textbook in database fail
#     def test_update_ISBN_fail(self):
#         response = self.client.post('/admin2', data = {'ISBNToUpdate': 'notindatabase','name':'new name', 'author': 'new author'})
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), 'ISBN not in database!')
