from django.shortcuts import render
from .models import Event
from accounts.models import User
from .forms import EventForm
from django.http import HttpResponse, HttpResponseRedirect


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

    # if not request.user.is_authenticated():
    #    return render(request, './accounts/templates/login.html')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            # Temporary - This only works becuase I first created an account and a sig
            # (The account I created had the first name "Zach")
            event.creator = User.objects.get(first_name="Zach")

            #event.creator = request.user
            event.save()
            return HttpResponseRedirect("/")
        else:
            return HttpResponse(form.errors)

    return render(request, 'events/create-event.html', {'form': EventForm})
