from . import actions
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase


class ActionsTestCase(TestCase):
    """
    Testing that various core actions work as intended.
    """
    def setUp(self):
        """
        Ensures the tests are set up properly before execution. 
        Initializes any required variables and data.

        :rtype: None.
        :return: None.
        """
        super().setUp()

    def test_actions_functions(self):
        """
        Tests member functions within actions.py.

        :rtype: None.
        :return: None.
        """
        valid_domains = getattr(settings, 'ENFORCED_EMAIL_DOMAINS', None)
        self.assertIsNotNone(valid_domains)

        for domain in valid_domains:
            self.assertEqual(actions.is_valid_email(r'test@'+domain), True)
            self.assertEqual(actions.is_valid_email(domain), False)
            self.assertEqual(actions.is_valid_email(r'@'+domain), False)

        self.assertEqual(actions.is_valid_email('test@thisisntavalidemail.com'), False)
        self.assertEqual(actions.is_valid_email('test'), False)
        self.assertEqual(actions.is_valid_email('@test.com'), False)
        self.assertEqual(actions.is_valid_email('.com'), False)

        with self.settings(ENFORCED_EMAIL_DOMAINS=None):
            with self.assertRaises(ImproperlyConfigured):
                actions.is_valid_email('test')

        with self.settings(ENFORCED_EMAIL_DOMAINS='test'):
            with self.assertRaises(ImproperlyConfigured):
                actions.is_valid_email('test@test')

        with self.assertRaises(TypeError):
            actions.is_valid_email()

class ViewTestCase(TestCase):
    """
    Testing correctness of core views.
    """
    
    def setUp(self):
        """
        Ensures the tests are set up properly before execution.
        Initializes any required variables and data.

        :rtype: None.
        :return: None.
        """
        super().setUp()

    def test_view_integrity(self):
        """
        Ensures that core views are raised under proper conditions.
        For example, 404.html should be displayed when a non-existent
        url is requested.

        :rtype: None.
        :return: None.
        """
        response = self.client.get('43214321432141')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

