from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.core.exceptions import ImproperlyConfigured 
from accounts.models import User

import hashlib
import os
import requests
import json
import base64
# Create your views here.

###
# TODO: Modular Authentication with support for different protocols
###
class SocialAuthIndex(View):
    """
    Default Social Authentication Class View which attempts to define the
    necessary elements for plug-and-play Social Authentication for any site.
    """

    http_method_names = ['get']

    auth_types = {
        'OAuth2': {
            'necessary-parms': [
                'redirect-uri',
                'client-id',
                'client-secret',
                'auth_endpoint',
                'token_endpoint',
                'auth_scope',
            ],
            'handler': 'oauth2'
        },
    }

    auth_patterns = {
        'google-oauth2': {
            'auth-type': 'OAuth2',
            'parms': {
                'redirect-uri': getattr(settings, 'GOOGLE_OAUTH2_REDIRECT_URI', None),
                'client-id': getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID'),
                'client-secret':getattr(settings, 'GOOGLE_OAUTH2_CLIENT_SECRET'),
                'auth_endpoint':'https://accounts.google.com/o/oauth2/v2/auth',
                'token_endpoint':'https://www.googleapis.com/oauth2/v4/token',
                'auth_scope':'openid email profile',
                'auth_hd':'mst.edu',
                'auth_response-type':''
            },
        },
    }
        
    def get(self, request, **kwargs):

        ###
        # If the user is authenticated, there is no reason to re-login
        ###
        if request.user.is_authenticated():
            return(HttpResponseRedirect('/'))

        backend = kwargs.get('auth_backend')
        auth_pattern = self.auth_patterns.get(backend)

        if(auth_pattern is not None):
            ###
            # Creates state comparator which ensures transaction integrity
            # between the server and a specific client 'state'
            ###
            state = hashlib.sha256(os.urandom(1024)).hexdigest()
            request.session['state'] = state
            ###
            # Formation of the authorization endpoint redirect for
            # Google OAuth2 Step 2 and then user redirect to authorize
            # ACM-General Registration App
            ###
            data = {
                'client_id': getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID'),
                'response_type':'code',
                'scope':'openid email profile',
                'redirect_uri':getattr(settings, 'GOOGLE_OAUTH2_REDIRECT_URI'),
                'state':state,
                'hd':'mst.edu',
            }
            request = requests.post(
                        'https://accounts.google.com/o/oauth2/v2/auth',
                        data=data)

            return HttpResponseRedirect(request.url)
        else:
            raise Http404("Authentication type does not exist")


class CallbackIndex(View):
     http_method_names = ['get']

     def get(self, request, **kwargs):
        """
        Google Callback URL which takes the POST data from google, cleans the
        data to python datatypes, and creates/finds the user with the data.

        For furthur information, see furthur information from Step 4 of:
        https://developers.google.com/identity/protocols/OpenIDConnect#server-flow
        """

        ###
        # Normalizing data from callback
        ###
        responseState = request.GET.get('state')
        sessionState = request.session['state']
        code = request.GET.get('code')

        ###
        # Ensure state integrity of the user
        ###
        if(responseState != sessionState): 
            return(HttpResponseRedirect(''))
        else:
            ###
            # Creates and POSTs token endpoint request for the user
            # JSON Web Token which contains the User Data
            ###
            payload = {
                'code':code,
                'scope':'',
                'client_id':getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID'),
                'client_secret':getattr(settings, 'GOOGLE_OAUTH2_CLIENT_SECRET'),
                'redirect_uri':getattr(settings, 'GOOGLE_OAUTH2_REDIRECT_URI'),
                'grant_type':'authorization_code',
            }
            tokenRequest = requests.post(
                    "https://www.googleapis.com/oauth2/v4/token", 
                data=payload)

        ###
        # Cleaning the JSON Web Token into usable python datatypes
        ###
        json_data = json.loads(tokenRequest.text) 
        JWTsegments = json_data['id_token'].split('.')
        userData = base64.urlsafe_b64decode(JWTsegments[1] + "==")
        cleaned_userData = json.loads((userData).decode('utf-8'))
        email = cleaned_userData['email']

        ###
        # Creating/Authenticating User from the JSON Web Token
        ###
        User.objects.get_or_create(email=email)
        user = authenticate(email=email)

        ###
        # Login for the User
        ###
        if user is not None:
            login(request, user)
        else:
            return(HttpResponse('Error'))

        return(HttpResponse('Ello'))
