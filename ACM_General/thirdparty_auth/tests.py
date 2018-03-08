"""
Contains unit tests for the thirdparty_auth.
"""
# third-party
import oauthlib
from importlib import import_module

# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse
from django.test import TestCase

# local Django
from accounts import models


class GoogleOAuth2AuthorizationTestCase(TestCase):
    """
    Ensure authorization view for Google OAuth2 works properly.
    """

    def check_messages_with_redirect(self, url, message):
        """
        Check the User for specific messages created with the messages
        framework and ensure a redirect to the homepage occurred.

        :param str url: The url to preform the get request
        :param str message: The message to check again the message framework
        """

        response = self.client.get(
            url,
            follow=True
        )

        message_list = list(messages.get_messages(response.wsgi_request))

        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")

        self.assertEqual(
            str(message_list[0]),
            message
        )

    def setUp(self):
        super().setUp()
        self.default_user = models.User.objects.get(email="acm@mst.edu")

    def test_already_authenticate_user_redirect(self):
        check_message = "You are already logged in."

        self.client.force_login(self.default_user)
        self.check_messages_with_redirect(
            reverse("thirdparty_auth:google"),
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

    def test_next_query_parameter(self):
        response = self.client.get(
            reverse("thirdparty_auth:google"),
            {REDIRECT_FIELD_NAME: reverse("thirdparty_auth:google")},
            follow=True
        )

        self.assertEqual(
            self.client.session[REDIRECT_FIELD_NAME],
            reverse("thirdparty_auth:google")
        )


class GoogleOAuth2CallbackTestCase(TestCase):
    """
    Ensure callback view for Google OAuth2 works properly.
    """
    def setUp(self):
        super().setUp()
        self.default_user = models.User.objects.get(email="acm@mst.edu")

    def check_messages_with_redirect(self, url, message, **kwargs):
        """
        Check the User for specific messages created with the messages
        framework and ensure a redirect to the homepage occurred.

        :param url: The url to preform the get request
        :type url: str
        :param message: The message to check again the message framework
        :type message: str
        :param kwargs: The get parameters to pass to the GET request
        """
        response = self.client.get(
            url,
            kwargs,
            follow=True
        )

        message_list = list(messages.get_messages(response.wsgi_request))

        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertEqual(
            str(message_list[0]),
            message
        )

    def create_session(self):
        session_engine = import_module(settings.SESSION_ENGINE)
        store = session_engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def check_popping_redirect_session_variable(self, session={}, params={}):
        self.create_session()
        session = self.client.session
        session[REDIRECT_FIELD_NAME] = reverse("thirdparty_auth:google-callback")
        session["verification_key"] = reverse("thirdparty_auth:google-callback")
        for sess_key, sess_value in session.items():
            session[sess_key] = sess_value
        session.save()

        self.assertTrue(self.client.session[REDIRECT_FIELD_NAME])
        self.client.get(
            reverse("thirdparty_auth:google-callback"),
            params,
            follow=True,
            secure=True
        )
        session = self.client.session
        self.assertIsNone(session.get(REDIRECT_FIELD_NAME))
        self.assertTrue(session.get("verification_key"))

    def test_fail_redict_on_already_authenticated(self):
        check_message = (
            "You are already logged in."
        )
        self.client.force_login(self.default_user)
        self.check_messages_with_redirect(
            reverse("thirdparty_auth:google-callback"),
            check_message
        )

    def test_fail_redirect_on_no_session_state(self):
        check_message = (
            "Something is wrong with your session, please refresh the page."
        )
        self.check_messages_with_redirect(
            reverse("thirdparty_auth:google-callback"),
            check_message
        )

    def test_fail_redirect_on_not_matching_session_state(self):
        check_message = (
            "Something is wrong with your session, please refresh the page."
        )
        state_var = "test"
        self.check_messages_with_redirect(
            reverse("thirdparty_auth:google-callback"),
            check_message,
            state=state_var
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

    def test_popping_redirect_session_variable(self):
        self.check_popping_redirect_session_variable()

    def test_popping_redirect_session_variable_when_logged_in(self):
        self.client.force_login(self.default_user)
        self.check_popping_redirect_session_variable()

    def test_popping_redirect_session_variable_when_logged_in_with_state(self):
        self.client.force_login(self.default_user)
        self.check_popping_redirect_session_variable(
            session={"state": "test"},
            params={"state": "test"}
        )

    def test_popping_redirect_session_variable_when_logged_in_with_invalid_state(self):
        self.client.force_login(self.default_user)
        self.check_popping_redirect_session_variable(
            session={"state": "test"},
        )

    def test_popping_redirect_session_variable_when_logged_in_with_mismatch_state(self):
        self.client.force_login(self.default_user)
        self.check_popping_redirect_session_variable(
            session={"state": "test"},
            params={"state": "not_test"},
        )
        # And that is as far as we can test with oauth currently, need to look
        # into mocking and other testing strategies
