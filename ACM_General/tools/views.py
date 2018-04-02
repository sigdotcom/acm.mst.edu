# Django
# from django.conf import settings
from django.shortcuts import render  # , redirect, reverse
# from django.utils import timezone

# local Django
# from events.models import Event


def membership(request):
    """
    Renders the template for the index page. With that is also grabs next
    events, the number of which depends on settings.MAX_HOME_FLIER_COUNT,
    that aren't past expiry.

    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: django.http.request.HttpRequest

    :return: The render template of the index page.
    :rtype: django.shortcut.render
    """

    return (
        render(
            request,
            'tools/membership.html',
        )
    )
