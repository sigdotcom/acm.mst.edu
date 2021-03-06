# standard library
# third-party
from googleapiclient.discovery import build
# import google.oauth2.credentials
import google_auth_oauthlib.flow

# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse

# local Django
from accounts.models import User
from core.actions import is_valid_email


class GoogleAuthorization(View):
    """
    Initial authorization for OAuth2. This view begins the OAuth2 flow
    transaction by redirecting the user to the proper token resource.

    See https://developers.google.com/identity/protocols/OAuth2 for more
    information about how the OAuth2 protocol works.
    """
    http_method_names = ["get"]

    @staticmethod
    def get(request):
        """
        Initial preparation of the user to authenticate with the google API.
        Completes step 1 of the OAuth2 protocol.

        :returns: Redirect the user to the google consent url or the index if
                  a failure occurs.
        :rtype: :class:`django.http.HttpResponseRedirect`
        """
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in.")
            return HttpResponseRedirect(reverse("home:index"))

        google_social_config = settings.SOCIAL_AUTH_SETTINGS["google"]
        FLOW = google_auth_oauthlib.flow.Flow.from_client_config(
            google_social_config["config"],
            scopes=google_social_config["scopes"],
            redirect_uri=request.build_absolute_uri(
                reverse("thirdparty_auth:google-callback")
            ),
        )

        authorization_url, state = FLOW.authorization_url(
            hd="mst.edu",
            access_type="offline",
            prompt="select_account",
            include_granted_scopes="true",
        )

        request.session["state"] = state
        redirect_to = request.GET.get(REDIRECT_FIELD_NAME)
        if redirect_to:
            request.session[REDIRECT_FIELD_NAME] = redirect_to

        return HttpResponseRedirect(authorization_url)


class GoogleCallback(View):
    http_method_names = ["get"]

    @staticmethod
    def get(request):
        """
        Collect the google authentication token after the user successfully
        provides consent. With this token, the backend queries google's servers
        for additional oauth2 information. Then, their
        :class:`~accounts.models.User` object is created with the information
        gathered. Completes steps 2 and 3 of the OAuth2 protocol.

        :returns: Redirect to the index with a message containing success or
                  failure message.
        :rtype: :class:`django.http.HttpResponseRedirect`
        """
        next_url = request.session.pop(REDIRECT_FIELD_NAME, reverse("home:index"))

        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in.")
            return HttpResponseRedirect(reverse("home:index"))

        state = request.session.get("state")
        if state is None or request.GET.get("state") != state:
            messages.error(
                request,
                "Something is wrong with your session, "
                "please refresh the page."
            )
            return HttpResponseRedirect(reverse("home:index"))

        authorization_response = request.build_absolute_uri()
        google_social_config = settings.SOCIAL_AUTH_SETTINGS["google"]
        FLOW = google_auth_oauthlib.flow.Flow.from_client_config(
            google_social_config["config"],
            scopes=google_social_config["scopes"],
            redirect_uri=request.build_absolute_uri(
                reverse("thirdparty_auth:google-callback")
            ),
        )
        FLOW.fetch_token(authorization_response=authorization_response)
        session = FLOW.authorized_session()
        user_info = session.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
        email = user_info.get("email", None)
        first_name = user_info.get("given_name", None)
        last_name = user_info.get("family_name", None)

        if(is_valid_email(email)):
            user = User.objects.get_or_create(
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            user = authenticate(email=email)

        if user is not None:
            login(request, user)
            messages.success(
                request,
                'You have been logged in, {}.'.format(user.get_short_name())
            )
        else:
            messages.warning(
                request,
                "An error occurred during login, please try again later."
            )
            return HttpResponseRedirect(reverse("home:index"))

        return HttpResponseRedirect(next_url)
