# standard library
import base64
import hashlib
import json
import os

# third-party
from googleapiclient.discovery import build
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests

# Django
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views import View
from django.urls import reverse

# local Django
from accounts.models import User
from core.actions import is_valid_email

from django.contrib import messages

###
# TODO: Modular Authentication with support for different protocols
#       As of right now the Views do not actually use the auth_backend
#       parameter.
###



class GoogleAuthorization(View):
    """
    Default Social Authentication Class View which attempts to define
    the necessary elements for plug-and-play Social Authentication for
    any format.
    """
    http_method_names = ["get"]

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in.")
            return HttpResponseRedirect(reverse("home:index"))

        FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
            scopes="openid email profile",
            redirect_uri=request.build_absolute_uri(
                reverse("thirdparty_auth:google-callback")
            ),
        )

        authorization_url, state = FLOW.authorization_url(
            hd="mst.edu",
            access_type="offline",
            prompt="select_account",
            include_granted_scopes="true"
        )
        request.session["state"] = state

        return HttpResponseRedirect(authorization_url)

class GoogleCallback(View):
    http_method_names = ["get"]

    def get(self, request, **kwargs):
        state = request.session.get("state")
        if state is None or request.GET["state"] != state:
            messages.error(
                request,
                "Something is wrong with your session, please refresh the page."
            )
            return HttpResponseRedirect(reverse("home:index"))

        authorization_response = request.build_absolute_uri()
        FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
            scopes="openid email profile",
            redirect_uri=request.build_absolute_uri(
                reverse("thirdparty_auth:google-callback")
            ),
            state=state,
        )
        FLOW.fetch_token(authorization_response=authorization_response)
        user_info_service = build(
            serviceName="oauth2", version="v2",
            credentials=FLOW.credentials
        )
        user_info = user_info_service.userinfo().get().execute()
        return HttpResponse(str(user_info))
