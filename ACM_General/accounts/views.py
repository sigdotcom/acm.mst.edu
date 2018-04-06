"""
Contains views to be rendered by the accounts app
"""

# Django
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render


def user_logout(request):
    """
    View called in order to log out a user.

    :param request: Request to log out a user.
    :type request: django.http.request.HttpRequest

    :return: Redirect to homepage.
    :rtype: :class:`django.http.HttpResponseRedirect`
    """
    logout(request)
    messages.success(request, "Successfully logged out.")
    return HttpResponseRedirect('/')
