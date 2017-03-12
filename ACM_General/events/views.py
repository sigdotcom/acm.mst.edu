from django.shortcuts import render
from . import models


def list_events(request):
    return(render(
        request,
        'events/listEvents.html',
        {'eventsList': models.Event.objects.all()}
    ))
