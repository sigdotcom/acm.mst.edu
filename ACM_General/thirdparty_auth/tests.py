"""
Contains unit tests for the thirdparty_auth.
"""
# third-party
import oauthlib

# Django
from django.contrib import messages
from django.urls import reverse
from django.test import TestCase

# local Django
from accounts import models


class GoogleOAuth2AuthorizationTestCase(TestCase):
    """
    Ensures that third party authorization methods behave as expected.
    """

    def setUp(self):
        super().setUp()
        self.default_user = models.User.objects.get(email="acm@mst.edu")

    def test_already_authenticate_user_redirect(self):
        check_message = "You are already logged in."

        self.client.force_login(self.default_user)
        response = self.client.get(
            reverse("thirdparty_auth:google"),
            follow=True
        )

        message_list = list(messages.get_messages(response.wsgi_request))

        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertEqual(
            str(message_list[0]),
            check_message
        )

    def test_google_redirect_on_success(self):
        response = self.client.get(
            reverse("thirdparty_auth:google"),
            follow=True
        )

        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertIn(
            "https://accounts.google.com", response.redirect_chain[0][0]
        )
        # Will not work due to the redirect url parameter
        self.assertEqual(response.status_code, 400)


class GoogleOAuth2CallbackTestCase(TestCase):
    """
    Ensures that third party authorization methods behave as expected.
    """

    def setUp(self):
        super().setUp()
        self.default_user = models.User.objects.get(email="acm@mst.edu")

    def test_fail_redirect_on_no_session_state(self):
        check_message = (
            "Something is wrong with your session, please refresh the page."
        )
        response = self.client.get(
            reverse("thirdparty_auth:google-callback"),
            follow=True
        )
        message_list = list(messages.get_messages(response.wsgi_request))

        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertEqual(
            str(message_list[0]),
            check_message
        )

    def test_fail_redirect_on_not_matching_session_state(self):
        check_message = (
            "Something is wrong with your session, please refresh the page."
        )
        state_var = "test"
        response = self.client.get(
            reverse("thirdparty_auth:google-callback"),
            {"state": state_var},
            follow=True
        )
        message_list = list(messages.get_messages(response.wsgi_request))

        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertEqual(
            str(message_list[0]),
            check_message
        )

    def test_error_on_matching_session_state(self):
        state_var = "test"
        session = self.client.session
        session["state"] = state_var
        session.save()

        with self.assertRaises(
            oauthlib.oauth2.rfc6749.errors.MissingCodeError
        ):
            self.client.get(
                reverse("thirdparty_auth:google-callback"),
                {"state": state_var},
                follow=True,
                secure=True
            )

        # And that is as far as we can test with oauth currently, need to look
        # into mocking and other testing strategies
