# standard library
import base64
import hashlib
import json
import os

# third-party
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests

# Django
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views import View

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
    http_method_names = ['get']

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            message.warning(request, "You are already logged in.")
            return HttpResponseRedirect(reverse("home:index"))

        social_auth_config = getattr(settings, "SOCIAL_AUTH_CONFIG")

        if social_auth_config is None:
            message.error(
                request,
                "An error has occurred. Please contact acm@mst.edu. "
                "(ERROR: CONFIG)"
            )
            return HttpResponseRedirect(reverse("home:index"))

        google_auth_config = social_auth_config.get("google", None)
        if google_auth_config is None:
            message.error(
                request,
                "An error has occurred. Please contact acm@mst.edu. "
                "(ERROR: CONFIG)"
            )
            return HttpResponseRedirect(reverse("home:index"))

        flow_data = {
            "client_id": google_auth_config["client_id"],
            "client_secret": google_auth_config["client_secret"],
            "redirect_uri": google_auth_config["redirect_uri"],
            "scopes": "openid email profile"
        }
        flow = google_auth_oauthlib.flow.Flow.OAuth2WebServerFlow(
            **flow_data
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            prompt='select_account',
            include_granted_scopes='true'
        )
        request.session["state"] = state

        return HttpResponseRedirect(authorization_url)

class GoogleCallback(View):
    http_method_names = ['get']

    def get(self, request, **kwargs):
        state = request.session["state"]

        flow_data = {
            "client_id": google_auth_config["client_id"],
            "client_secret": google_auth_config["client_secret"],
            "redirect_uri": google_auth_config["redirect_uri"],
            "scopes": "openid email profile"
            "state": state
        }

        flow = google_auth_oauthlib.flow.Flow.OAuth2WebServerFlow(
            **flow_data
        )

        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)
        return str(flow.credentials)

