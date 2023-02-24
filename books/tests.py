from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse

from .models import Book, Review

class BookTests(TestCase):

        

    def setUp(self):
        self.book = Book.objects.create(
            title = 'Harry Potter',
            author= 'Jk Rowling',
            price = '25.00',
        )

        url = reverse('book_list')
        self.response = self.client.get(url)

        self.user = get_user_model().objects.create(
            username='testuser',
            email = 'testemail@email.com',
            password = 'testpassword'
        )

        self.special_permission = Permission.objects.get(codename='special_status')

        self.review = Review.objects.create(
            book = self.book,
            author = self.user,
            review = 'this is a review'

        )

    
    
    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'Jk Rowling')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email="testemail@email.com", password='testpassword')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_list_view_for_logged_out_user(self):
        self.client.logout()
        self.assertEqual(self.response.status_code, 302)
        self.assertRedirects(self.response, '%s?next=/books/' % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/books/' % (reverse('account_login'))
        )
        self.assertContains(response, 'Login')


    def test_book_detail_view_with_permission(self):
        self.client.login(email="testemail@email.com", password="testpassword")
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/book/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'this is a review')
        self.assertTemplateUsed(response, 'books/book_detail.html')
        self.assertContains(response, 'Harry Potter')
        
        

# Create your tests here.
