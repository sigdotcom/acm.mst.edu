# Django
from django.conf import settings
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse

# local Django
from accounts import models


class ViewTestCase(LiveServerTestCase):
    """
    Ensures that third party authroization methods behave as expected.
    """
    def setUp(self):
        """
        Initializes all variables and data required to test 
        third party authorizarion functionality.

        :rtype: None
        :return: None
        """
        super().setUp()
        self.user=models.User.objects.create(
                    email="test@mst.edu",
                    first_name="test_me",
                    last_name="test_please",
                )

    def test_view_integrity(self):
        """
        Ensures that third party authorization methods are handled
        correctly in the case of both proper and improper attempts.

        :rtype: None
        :return: None
        """
        ##
        # Testing initial login fails because of callback url
        ##
        response=self.client.get(reverse('thirdparty_auth:login',
                                 kwargs={
                                    'auth_type':'oauth2',
                                    'auth_provider':'google'
                                   }
                                ),
                                follow=True
                            )
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertIn(response.status_code, (404, 400))


        ##
        # Testing logged-in user being redirected
        ##
        self.client.force_login(self.user, backend='accounts.backends.UserBackend')
        response=self.client.get(reverse('thirdparty_auth:login',
                                 kwargs={
                                    'auth_type':'oauth2',
                                    'auth_provider':'google'
                                   }
                                ),
                                follow=True
                            )
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.client.logout()

        ##
        # Testing that invalid auth_provider gives 404
        ##
        response=self.client.get(reverse('thirdparty_auth:login',
                                         kwargs={
                                            'auth_type':'oauth2',
                                            'auth_provider':'test'
                                         }
                                    )
                                )
        self.assertEqual(response.status_code, 404)

        ##
        # Testing post-authentication oauth2 which cannot be attained through
        # integration tests without a fake google account.
        ##
        response=self.client.get(reverse('thirdparty_auth:callback',
                                         kwargs={
                                             'auth_type':'oauth2',
                                             'auth_provider':'google',
                                         }
                                    ),
                                    follow=True
                                )
        self.assertEqual(response.status_code, 404)

        ##
        # Testing invalid auth_provider
        ##
        response=self.client.get(reverse('thirdparty_auth:callback',
                                         kwargs={
                                             'auth_type':'oauth2',
                                             'auth_provider':'test',
                                         }
                                    ),
                                    follow=True
                                )
        self.assertEqual(response.status_code, 404)

        ##
        # Testing session-state authentication which is used to ensure a
        # proper user
        ##
        session = self.client.session
        session['state'] = 'test'
        session.save()
        response=self.client.get(reverse('thirdparty_auth:callback',
                                         kwargs={
                                             'auth_type':'oauth2',
                                             'auth_provider':'google',
                                         }
                                    ),
                                    {'state': 'test'},
                                    follow=True
                                )
        self.assertEqual(response.status_code, 404)

        ##
        # Testing Session-state with a bad auth_provider
        ##
        response=self.client.get(reverse('thirdparty_auth:callback',
                                         kwargs={
                                             'auth_type':'oauth2',
                                             'auth_provider':'test',
                                         }
                                    ),
                                    {'state': 'test'},
                                    follow=True
                                )
        self.assertEqual(response.status_code, 404)

        ##
        # TODO: Make a test which can properly bypass the JSON Web token
        #       request to the Google API servers on line 137 of views.py
        #       as of 3/26/17.
        ##
