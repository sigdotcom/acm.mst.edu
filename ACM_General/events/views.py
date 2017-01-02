from django.shortcuts import render
from events.models import Event

from datetime import datetime

def list_events(request):
    return(render(
        request,
        'events/listEvents.html',
        {'eventsList': Event.objects.all()}
    ))
