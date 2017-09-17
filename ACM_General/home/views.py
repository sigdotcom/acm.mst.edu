# Django
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

# local Django
from events.models import Event


def index(request):
    """
    Renders the template for the index page. With that is also grabs next
    events, the number of which depends on settings.MAX_HOME_FLIER_COUNT,
    that aren't past expiry.
    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: django.http.request.HttpRequest
    :rtype: django.shortcut.render
    :return: The render template of the index page.
    """ 

    events = Event.objects.filter(
        date_expire__gte=timezone.now()
    ).order_by('date_hosted')

    if len(events) >= settings.MAX_HOME_FLIER_COUNT:
        events = events[:settings.MAX_HOME_FLIER_COUNT]

    return (
        render(
            request,
            'home/index.html',
            {"upcoming_events": events}
        )
    )


def sponsors(request):
    """
    Handles a request to see the sponsors page.
    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: django.http.request.HttpRequest
    :rtype: django.shortcut.render
    :return: The render template of the sponsors page.
    """
    return (
        render(
            request,
            'home/sponsors.html',
        )
    )

def media(request):
    """
    Handles a request to see the media page.
    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: django.http.request.HttpRequest
    :rtype: django.shortcut.render
    :return: The render template of the media page.
    """
    return (
        render(
            request,
            'home/media.html',
        )
    )


def officers(request):
    """
    Handles a request to see the officers page.
    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: django.http.request.HttpRequest
    :rtype: django.shortcut.render
    :return: The render template of the officers page.
    """
    return (
        render(
            request,
            'home/officers.html',
        )
    )


def membership(request):
    """
    Handles a request to see the membership page.
    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: django.http.request.HttpRequest
    :rtype: django.shortcut.render
    :return: The render template of the officers page.
    """
    return (
        render(
            request,
            'home/membership.html',
        )
    )


def sigs(request):
    return (
        render(
            request,
            'home/sigs.html',
        )
    )