# Django
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

# local Django
from events.models import Event


def index(request):
    # Grabs the 3 nearest upcoming events that haven't expired yet
    events = Event.objects.filter(date_expire__gte=timezone.now()).order_by('date_hosted')
    if len(events) >= settings.MAX_HOME_FLIER_COUNT:
        events = events[:settings.MAX_HOME_FLIER_COUNT]

    return(render(
        request,
        'home/index.html',
        {"upcoming_events": events}
    ))


def sponsors(request):
    return (
        render(
            request,
            'home/sponsors.html',
        )
    )


def calendar(request):
    return (
        render(
            request,
            'home/calendar.html',
        )
    )


def media(request):
    return (
        render(
            request,
            'home/media.html',
        )
    )


def officers(request):
    return (
        render(
            request,
            'home/officers.html',
        )
    )


def membership(request):
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
