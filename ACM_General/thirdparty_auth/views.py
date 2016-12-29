from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse 
import hashlib
import os
import requests
# Create your views here.

def index(request, auth_backend):
    
 
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
        
        return(HttpResponse(type(request.json())))
        return(HttpResponseRedirect(request.url))

def googleCallback2(request):
    return( HttpResponse(request.POST))
