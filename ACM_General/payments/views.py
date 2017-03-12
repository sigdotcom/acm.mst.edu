from django.http import HttpResponseRedirect
from django.views import View

# Create your views here.


class SodamachinePayment(View):
    """
    TODO: Docstring
    """
    @staticmethod
    def get():
        return HttpResponseRedirect('https://acm-chat.mst.edu/')
