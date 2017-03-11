from django.shortcuts import render

# Create your views here.


def index(request):
    return(render(
        request,
        'home/index.html',
    ))


def sponsors(request):
    return(render(
        request,
        'home/sponsors.html',
    ))


def calendar(request):
    return(render(
        request,
        'home/calendar.html',
    ))
