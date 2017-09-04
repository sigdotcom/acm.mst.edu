# standard library
import os

# third-party
import stripe

# Django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View

# local Django
from . import models


class MembershipPayment(View):
    def get(self, request):
        """
        TODO: Docstring
        """
        return render(
                request,
                'payments/acm_membership.html',
                {
                    "products": models.Product.objects.all(),
                    "stripe_public_key": getattr(settings, 'STRIPE_PUB_KEY', None)
                }
            )


class ProductHandler(View):
    def post(self, request, pk):
        """
        TODO: Docstring
        """
        token = request.POST.get('stripeToken', None)
        if request.user.is_authenticated() == False:
            raise Http404("Invalid User")

        if token is None:
            raise ValueError('ProductHandler view did not receive a stripe'
                             ' token in the POST request.')

        stripe.api_key = getattr(settings, 'STRIPE_PRIV_KEY' , None)
        if(stripe.api_key == "" or stripe.api_key == None):
            raise ValueError('ProductHandler view has an invalid'
                             ' stripe.api_key, please insert one in'
                             ' settings_local.py.')

        product = get_object_or_404(models.Product, pk=pk)
        charge = stripe.Charge.create(
                    currency="usd",
                    amount=int(product.cost*100),
                    description=product.description,
                    source=token,
                )

        trans = models.Transaction.objects.create_transaction(
                                        token, user=request.user,
                                        cost=product.cost,
                                        sig=product.sig,
                                        category=product.category,
                                        description=product.description
                                    )

        return HttpResponseRedirect('/')
