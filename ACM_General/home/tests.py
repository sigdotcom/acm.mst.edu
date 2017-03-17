from django.urls import reverse
from django.test import TestCase

# Create your tests here.

class HomeViewCase(TestCase):
    def setUp(self):
        super(TestCase, self).setUp()

    def test_view_responses(self):
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

        response = self.client.get(reverse('home:sponsors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/sponsors.html')

        response = self.client.get(reverse('home:calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/calendar.html')

