from django.test import TestCase
from django.urls import reverse

from .models import Book

class BookTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title = 'Harry Potter',
            author= 'Jk Rowling',
            price = '25.00',
        )

        url = reverse('book_list')
        self.response = self.client.get(url)
    
    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'Jk Rowling')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'Harry Potter')
        self.assertTemplateUsed(self.response, 'books/book_list.html')

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/book/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'books/book_detail.html')
        self.assertContains(response, 'Harry Potter')
        
        

# Create your tests here.
