from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse

class HomePageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_homepage_url_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')
    
    #to check there is no incorrect html
    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'i should not be here'
        )

# Create your tests here.
