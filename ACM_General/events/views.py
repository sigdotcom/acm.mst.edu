from django.shortcuts import render
from .models import Event
from accounts.models import User
from .forms import EventForm
from django.http import HttpResponse, HttpResponseRedirect
from accounts.backends import UserBackend
from django.contrib.auth import login


def list_events(request):
    """
    This function is used for creating a view that lists out all of the events
    in an organized manner.

    :return: An HTML rendered page of 'listEvents.html' that has all of the
             Event objects passed into it.
    """
    return render(request, 'events/listEvents.html', {'eventsList': Event.objects.all()})


def create_event(request):
    """
    This funciton is used for authenticating users who have permission to
    create events as well as actually adding the created event to the database.
    """

    # Used for testing purposes
    #user = UserBackend().authenticate('zdw27f@mst.edu')
    #request.user = user

    # Temporary (until permissions are setup): makes sure the user attempting
    # to create an event is a superuser.
    if not request.user.is_superuser:
        return render(request, '404.html')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        # Validates form and adds creator to event
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return HttpResponseRedirect("/")
        else:
            return HttpResponse(form.errors)

    # Sends user to create event page if the user has permission to do so along
    # with the request not being a POST request (not submitting the form).
    return render(request, 'events/create-event.html', {'form': EventForm})
