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
        'scope':'openid email',
        'redirect_uri':getattr(settings, 'GOOGLE_OAUTH2_REDIRECT_URI'),
        'state':state,
        'hd':'mst.edu',
    }
    request.session['state'] = state
    request = requests.get(
                'https://accounts.google.com/o/oauth2/v2/auth',
                params=data)

    return HttpResponseRedirect(request.url)
    

def googleCallback(request):
    pass
