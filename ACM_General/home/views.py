"""
Contains all of the view for the Home app.
"""
# Django
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.utils import timezone

# local Django
from events.models import Event
# from accounts.backends import UserBackend


def index(request):
    """
    Renders the template for the index page. With that is also grabs next
    events, the number of which depends on settings.MAX_HOME_FLIER_COUNT,
    that aren't past expiry.

    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: :class:`~django.http.request.HttpRequest`

    :return: The render template of the index page.
    :rtype: `django.shortcut.render`
    """
    # request.user = UserBackend().authenticate('cmm4hf@mst.edu')

    events = Event.objects.filter(
        date_expire__gte=timezone.now()
    ).order_by('date_hosted')

    num_events = len(events)
    if len(events) >= settings.MAX_HOME_FLIER_COUNT:
        events = events[:settings.MAX_HOME_FLIER_COUNT]

    return (
        render(
            request,
            'home/index.html',
            {
                "upcoming_events": events,
                "num_events": num_events
            }
        )
    )


def sponsors(request):
    """
    Handles a request to see the sponsors page.

    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: :class:`~django.http.request.HttpRequest`

    :return: The render template of the sponsors page.
    :rtype: `django.shortcut.render`
    """
    return (
        render(
            request,
            'home/sponsors.html',
        )
    )


def calendar(request):
    """
    Handles a request to see the calendar page. Updated to redirect to the
    front page.

    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: :class:`~django.http.request.HttpRequest`

    :return: A redirect to the homepage with a ``#calendar`` anchor which will
             automatically put the user's page onto the calendar.
    :rtype: `django.shortcut.redirect`
    """
    return (
        redirect(
            reverse('home:index') + "#calendar",
            permanent=True,
        )
    )


def media(request):
    """
    Handles a request to see the media page.

    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: :class:`django.http.request.HttpRequest`

    :return: The render template of the media page.
    :rtype: `django.shortcut.render`
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
    :type request: :class:`django.http.request.HttpRequest`

    :return: The render template of the officers page.
    :rtype: `django.shortcut.render`
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
    :type request: :class:`~django.http.request.HttpRequest`

    :return: The render template of the officers page.
    :rtype: `django.shortcut.render`
    """
    return (
        render(
            request,
            'home/membership.html',
        )
    )


def sigs(request):
    """
    Handles a request to see the sigs page.

    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: :class:`~django.http.request.HttpRequest`

    :return: The render template of the sigs page.
    :rtype: `django.shortcut.render`
    """
    return (
        render(
            request,
            'home/sigs.html',
        )
    )
