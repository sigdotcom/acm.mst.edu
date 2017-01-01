from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse 
from django.contrib.auth import authenticate, login
from accounts.models import User
import hashlib
import os
import requests
import json
import base64
# Create your views here.

def index(request, auth_backend):
    if request.user.is_authenticated():
        return(HttpResponse('No way hosea'))
 
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    data = {
        'client_id': getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID'),
        'response_type':'code',
        'scope':'openid email profile',
        'redirect_uri':getattr(settings, 'GOOGLE_OAUTH2_REDIRECT_URI'),
        'state':state,
        'hd':'mst.edu',
    }
    request.session['state'] = state
    request = requests.post(
                'https://accounts.google.com/o/oauth2/v2/auth',
                data=data)

    return HttpResponseRedirect(request.url)
    

def googleCallback(request):
    responseState = request.GET.get('state')
    sessionState = request.session['state']
    code = request.GET.get('code')

    if(responseState != sessionState): 
        return(HttpResponseRedirect(''))
    else:
        payload = {
            'code':code,
            'scope':'',
            'client_id':getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID'),
            'client_secret':getattr(settings, 'GOOGLE_OAUTH2_CLIENT_SECRET'),
            'redirect_uri':getattr(settings, 'GOOGLE_OAUTH2_REDIRECT_URI'),
            'grant_type':'authorization_code',
        }
        request = requests.post(
                "https://www.googleapis.com/oauth2/v4/token", 
                data=payload)

        json_data = json.loads(request.text) 
        JWTsegments = json_data['id_token'].split('.')
        userData = base64.urlsafe_b64decode(JWTsegments[1] + "==")
        cleaned_userData = json.loads((userData).decode('utf-8'))
        user, didCreate = User.objects.get_or_create(email=cleaned_userData['email'])

        user = authenticate(email=cleaned_userData['email'])
        request.session

        if user is not None:
            login(request, user)
        else:
            return(HttpResponse('Error'))


        return(HttpResponse('Ello'))
