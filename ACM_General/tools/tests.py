"""
Contains all unit tests for the Tools app.
"""

# Django
# from django.conf import settings
# from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
# from django.utils import timezone

# local Django
# from accounts.models import User
# from events.forms import EventForm
# from sigs.models import SIG
# from events.models import Event


class HomeViewCase(TestCase):
    """
    A class that tests whether tools functions work
    """

    def test_view_responses(self):
        """
        Makes requests to each page of the site and asserts a 200 response code
        (or success)
        """
        response = self.client.get(reverse('tools:membership'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tools/membership.html')
