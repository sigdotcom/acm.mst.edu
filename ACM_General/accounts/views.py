# Django
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render


def user_logout(request):
    """
    View called in order to log out a user followed by a
    redirect to the base url.

    :param request: Request to log out a user.
    :type request: Request
    :rtype: Response
    :return: Redirect to the base url, '/'.
    """
    logout(request)
    return HttpResponseRedirect('/')


def user_login(request):
    """
    View rendered that displays third party login options.

    :param request: Request to log in a user.
    :type request: Request
    :rtype: Response
    :return: Template displaying third party login options.
    """
    return render(request, "accounts/login.html")
