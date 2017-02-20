from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
import stripe

# Create your views here.

class membershipPayments(View):
    def get(self, request):
        return render(request,'payments/payment.html', {})

class paymentCallback(View):
    def post(self, request, amount):
        token = request.POST['stripeToken']
        charge = stripe.Charge.create(
                    currency="usd",
                    amount=str(amount),
                    description="ACM Membership Charge",
                    source=token,
                )
        return HttpResponse(charge['failure_message'])
