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


def media(request):
    return(render(
        request,
        'home/media.html',
    ))


def officers(request):
    return (render(
        request,
        'home/officers.html',
    ))


def membership(request):
    return (render(
        request,
        'home/membership.html',
    ))
