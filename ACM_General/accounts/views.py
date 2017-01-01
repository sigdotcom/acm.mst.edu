from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.contrib.auth import logout

# Create your views here.

def user_logout(request):
    logout(request)
    return(HttpResponseRedirect('/'))
