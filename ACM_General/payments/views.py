# standard library

# third-party
import stripe

# Django
from django.conf import settings
# from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
from accounts.backends import UserBackend

# local Django
from . import models


class ProductHandler(View):
    """
    View meant for handling requests related to products & transactions.
    """

    def post(self, request, tag):
        """
        This view submits a Stripe transaction and its to the database.

        :type request: django.http.request.HttpRequest
        :param request: Request object that contains information from the
                        user's POST/GET request.

        :raises ValueError: If the stripe token is empty or if the stripe
                               api key is invalid.
        :raises Http404: If an unauthenticated user attempts to access the
                            page.

        :rtype: django.http.HttpResponseRedirect or django.http.Http404
        :returns: Html page redirection to the index page or the 404 error page
                  (if the user was authenticated).
        """
        request.user = UserBackend().authenticate("ksyh3@mst.edu")

        if not request.user.is_authenticated():
            raise Http404("Invalid User")

        token = request.POST.get('stripeToken', None)
        if token is None:
            raise ValueError('ProductHandler view did not receive a stripe'
                             ' token in the POST request.')

        stripe.api_key = getattr(settings, 'STRIPE_PRIV_KEY', None)
        if stripe.api_key == "" or not stripe.api_key:
            raise ValueError('ProductHandler view has an invalid'
                             ' stripe.api_key, please insert one in'
                             ' settings_local.py.')

        product = get_object_or_404(models.Product, tag=tag)
        stripe.Charge.create(
            currency="usd",
            amount=int(product.cost * 100),
            description=product.description,
            source=token,
        )

        models.Transaction.objects.create_transaction(
            token, user=request.user,
            cost=product.cost,
            sig=product.sig,
            category=product.category,
            description=product.description
        )

        return HttpResponseRedirect('/')
