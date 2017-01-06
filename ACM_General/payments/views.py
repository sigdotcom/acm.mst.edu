from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

# Create your views here.

class sodamachinePayment(View):
    def get(self, request):
        return HttpResponseRedirect('https://acm-chat.mst.edu/')
