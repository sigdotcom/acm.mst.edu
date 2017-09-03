# Django
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_login(request):
    return render(request, "accounts/login.html")
