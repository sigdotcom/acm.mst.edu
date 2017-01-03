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
#       As of right now the Views do not actually use the auth_backend
#       parameter.
###
class AuthorizationView(View):
    """
    @Desc: Default Social Authentication Class View which attempts to define
           the necessary elements for plug-and-play Social Authentication for 
           any format.
    """

    http_method_names = ['get']

    auth_methods = {
        'google-oauth2': ''
    }

    def get(self, request, **kwargs):
        """
        @Desc: OAuth authorization processing and transaction handler.

        @Returns: Prepared GET/POST redirect to the OAuth authentication
                  endpoint.
        """

        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        backend = kwargs.get('auth_backend')
        auth_pattern = self.auth_methods.get(backend)

        if(auth_pattern is not None):
            data = self.prepare_transaction(request, backend)
            request = requests.post(
                        'https://accounts.google.com/o/oauth2/v2/auth',
                        data=data
                      )

            return HttpResponseRedirect(request.url)
        else:
            raise Http404("Authentication type does not exist")

    def prepare_transaction(self, request, auth_backend):
        """
        @Desc: Prepares the POST/GET request parameters for the initial
               authorization request for OAuth2. Also, Creates state comparator
               which ensures transaction integrity between the server and a 
               specific client 'state'.

        @Returns: Returns a dictonary of the necessay POST/GET parameters
                  for an authorization request.
        """
        state = hashlib.sha256(os.urandom(1024)).hexdigest()
        request.session['state'] = state

        data = {
            'client_id': getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID'),
            'response_type':'code',
            'scope':'openid email profile',
            'redirect_uri':getattr(settings, 'GOOGLE_OAUTH2_REDIRECT_URI'),
            'state':state,
            'hd':'mst.edu',
        }

        return data

class TokenView(View):
    """
    @Desc: Default Token Transaction View which handles the token OAuth
           transaction as well as User registration/login for each User
           authenticated
    """
    http_method_names = ['get']


    def get(self, request, **kwargs):
        """
        @Desc: Google Callback URL which takes the POST data from google, 
               cleans the data to python datatypes, and creates/finds the user 
               with the data.

               For furthur information, see Step 4 of:
               https://developers.google.com/identity/protocols/OpenIDConnect#server-flow
        """
        ###
        # Normalizing data from callback
        ###
        responseState = request.GET.get('state')
        sessionState = request.session['state']
        auth_backend = kwargs.get('auth_backend')

        ###
        # Ensure state integrity of the user
        ###
        if(responseState != sessionState): 
            return(HttpResponseRedirect(''))

        payload = self.prepare_transaction(request, auth_backend)
        tokenRequest = requests.post(
                            "https://www.googleapis.com/oauth2/v4/token", 
                            data=payload
                       )
        cleaned_data = self.clean_JWT(tokenRequest.text)

        self.post_auth(request, cleaned_data)



    def prepare_transaction(self, request, auth_backend):
        """
        @Desc: Preparing the GET/POST data necessary to perform the Token
               Transaction.

        @Returns: Returns the GET/POST data necessary to perform the Token
                  Transaction.
        """
        code = request.GET.get('code')

        payload = {
            'code':code,
            'scope':'',
            'client_id':getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID'),
            'client_secret':getattr(settings, 'GOOGLE_OAUTH2_CLIENT_SECRET'),
            'redirect_uri':getattr(settings, 'GOOGLE_OAUTH2_REDIRECT_URI'),
            'grant_type':'authorization_code',
        }

        return(payload)

    def clean_JWT(self, text):
        """
        @Desc: Transforms text containing a JSON Web Token into a cleaned
               python dictionary.

        @Returns: Returns the clean JSON Web Token as a python dictionary.
        """
        json_data = json.loads(text) 
        JWTsegments = json_data['id_token'].split('.')
        userData = base64.urlsafe_b64decode(JWTsegments[1] + "==")
        cleaned_userData = json.loads((userData).decode('utf-8'))

        return(cleaned_userData)

    def post_auth(self, request, cleaned_data):
        """
        @Desc: Actions after the JSON Web Token has been cleaned and the rest
               of the transaction has been properly authenticated. Should be
               used to perform some post_auth action and then present some
               template/redirect.
        """
        email = cleaned_data.get('email') 
        first_name = cleaned_data.get('given_name')
        last_name = cleaned_data.get('family_name')

        User.objects.get_or_create(
            email=email, 
            first_name=first_name,
            last_name=last_name,
        )
        user = authenticate(email=email)

        if user is not None:
            login(request, user)
        else:
            return(HttpResponse('Error'))

        return(HttpResponseRedirect('/'))

