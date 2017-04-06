from django.shortcuts import render
from .models import Event
from accounts.models import User
from datetime import datetime
from .forms import EventForm
from django.http import HttpResponse, HttpResponseRedirect


def list_events(request):
    return(render(
        request,
        'events/listEvents.html',
        {'eventsList': Event.objects.all()}
    ))


def create_event(request):
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
