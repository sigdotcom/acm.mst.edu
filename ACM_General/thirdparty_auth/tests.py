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


class SocialAuthTestCase(TestCase):
    """
    Generic Social Authentication test case which provides useful generic
    functions to testing the authentication cases.
    """
    def setUp(self):
        super().setUp()

    def assert_redirect(self, url, template=None, **kwargs):
        """
        Asserts that the Client was sucessfully redirected to the specified URL
        and verify the template if specified.

        :param url: The URL to perform the initial GET request on
        :type url: string
        :param template: The template to assert the final URI uses. For example:
            "home/index.html".
        :type template: string
        :param kwargs: Extra query parameters to include in the GET parameters.
        :type kwargs: dict

        :returns: The Client's response from the GET request.
        :rtype: :class:`django.core.handlers.wsgi.WSGIRequest`
        """
        response = self.client.get(
            url,
            kwargs,
            follow=True
        )
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)
        if template:
            self.assertTemplateUsed(response, template)

        return response

    def check_messages_with_redirect(self, url, message, template=None, **kwargs):
        """
        Check the User for specific messages created with the messages
        framework and ensure a redirect to the homepage occurred.

        :param url: The url to perform the get request
        :type url: str
        :param message: The message to check again the message framework
        :type message: str
        :param kwargs: The get parameters to pass to the GET request
        """
        response = self.assert_redirect(url, template=template)
        message_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(
            str(message_list[0]),
            message
        )

    def create_session(self):
        """
        Use the session module to create a persistant session for the Django
        Test Client.
        """
        session_engine = import_module(settings.SESSION_ENGINE)
        store = session_engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def check_popping_redirect_session_variable(self, session_vals=None, params=None):
        """
        Ensures that the REDIRECT_FIELD_NAME session key is removed from the
        client's session whenever the Client reaches the callback page.

        :param session: Extra session variables to attach to the Client's
            session
        :type session: dict
        :param params: Query parameters to include in the GET request to the
            callback URL.
        :type params: dict
        """
        self.create_session()
        session_vals = session_vals or dict()
        params = params or dict()
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


class GoogleOAuth2AuthorizationTestCase(SocialAuthTestCase):
    """
    Ensure authorization view for Google OAuth2 works properly.
    """

    def setUp(self):
        super().setUp()
        self.default_user = models.User.objects.get(email="acm@mst.edu")

    def test_already_authenticate_user_redirect(self):
        check_message = "You are already logged in."

        self.client.force_login(self.default_user)
        self.check_messages_with_redirect(
            reverse("thirdparty_auth:google"),
            check_message,
            template="home/index.html",
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


class GoogleOAuth2CallbackTestCase(SocialAuthTestCase):
    """
    Ensure callback view for Google OAuth2 works properly.
    """
    def setUp(self):
        super().setUp()
        self.default_user = models.User.objects.get(email="acm@mst.edu")

    def test_fail_redict_on_already_authenticated(self):
        check_message = (
            "You are already logged in."
        )
        self.client.force_login(self.default_user)
        self.check_messages_with_redirect(
            reverse("thirdparty_auth:google-callback"),
            check_message,
            template="home/index.html",
        )

    def test_fail_redirect_on_no_session_state(self):
        check_message = (
            "Something is wrong with your session, please refresh the page."
        )
        self.check_messages_with_redirect(
            reverse("thirdparty_auth:google-callback"),
            check_message,
            template="home/index.html",
        )

    def test_fail_redirect_on_not_matching_session_state(self):
        check_message = (
            "Something is wrong with your session, please refresh the page."
        )
        state_var = "test"
        self.check_messages_with_redirect(
            reverse("thirdparty_auth:google-callback"),
            check_message,
            template="home/index.html",
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
            session_vals={"state": "test"},
            params={"state": "test"}
        )

    def test_popping_redirect_session_variable_when_logged_in_with_invalid_state(self):
        self.client.force_login(self.default_user)
        self.check_popping_redirect_session_variable(
            session_vals={"state": "test"},
        )

    def test_popping_redirect_session_variable_when_logged_in_with_mismatch_state(self):
        self.client.force_login(self.default_user)
        self.check_popping_redirect_session_variable(
            session_vals={"state": "test"},
            params={"state": "not_test"},
        )

    def test_sucessful_redirect(self):
        """
        Cannot test due to google oauth2 blocking, need to find a solution
        around it.
        """
        pass

        # And that is as far as we can test with oauth currently, need to look
        # into mocking and other testing strategies
