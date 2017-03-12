from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from django.shortcuts import render
from . import models
from . import forms
import stripe

# Create your views here.

stripe.api_key = getattr(settings, 'STRIPE_KEY' , None)

if(stripe.api_key == None):
    raise ImproperlyConfigured('Please enter a Stripe API key into settings_local')


class MembershipPayment(View):
    def get(self, request):
        """
        TODO: Docstring
        """

        return render(
                request,
                'payments/acm_membership.html',
                {"products": models.Product.objects.all()}
            )


class paymentCallback(View):
    def post(self, request, amount):
        """
        TODO: Docstring
        """

        token = request.POST['stripeToken']
        charge = stripe.Charge.create(
                    currency="usd",
                    amount=str(amount),
                    description="ACM Membership Charge",
                    source=token,
                )

        trans = models.Transaction.objects.create_transaction(
                                        token, user = request.user,
                                        cost = amount,
                                        category = 'ACM Membership (Year)',
                                        description = 'See Category',
                                    )

        return HttpResponse(trans)

