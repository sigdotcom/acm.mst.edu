from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from . import forms

# Create your views here.


class SodamachinePayment(View):
    """
    TODO: Docstring
    """
    @staticmethod
    def get():
        return HttpResponseRedirect('https://acm-chat.mst.edu/')


class MembershipPayment(View):
    """
    TODO: Docstring
    """
    def get(self, request):
        return render(request,
                      "payments/acm_membership.html",
                      {'form': forms.MembershipForm},
                     )

