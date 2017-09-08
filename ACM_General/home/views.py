# Django
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

# local Django
from events.models import Event


def index(request):
    """
        Grabs the next 3 events that aren't past expiry,
        then redirect to the index.

        :param request: Request for index page with upcoming events.
        :type request: Request
        :rtype: Response
        :return: Redirect to the base url with events, '/'.
    """
      
    events = Event.objects.filter(date_expire__gte=timezone.now()).order_by('date_hosted')
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

        :param request: Request for the sponsors page.
        :type request: Request
        :rtype: Response
        :return: Redirect to the sponsors page, '/'.
    """
    return (
        render(
            request,
            'home/sponsors.html',
        )
    )


def calendar(request):
    """
        Handles a request to see the calendar page.

        :param request: Request for the calendar page.
        :type request: Request
        :rtype: Response
        :return: Redirect to the calendar page, '/'.
    """
    return (
        render(
            request,
            'home/calendar.html',
        )
    )


def media(request):
    """
        Handles a request to see the media page.

        :param request: Request for the media page.
        :type request: Request
        :rtype: Response
        :return: Redirect to the media page, '/'.
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

        :param request: Request for the officers page.
        :type request: Request
        :rtype: Response
        :return: Redirect to the officers page, '/'.
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

        :param request: Request for the membership page.
        :type request: Request
        :rtype: Response
        :return: Redirect to the membership page, '/'.
    """
    return (
        render(
            request,
            'home/membership.html',
        )
    )
