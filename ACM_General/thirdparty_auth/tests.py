from accounts import models
from django.conf import settings
from django.urls import reverse
from django.test import TestCase, LiveServerTestCase

# Create your tests here.

class ViewTestCase(LiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.user=models.User.objects.create(
                    email="test@mst.edu",
                    first_name="test_me",
                    last_name="test_please",
                )

    def test_view_integrity(self):
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
        self.assertEqual(response.status_code, 404)


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


