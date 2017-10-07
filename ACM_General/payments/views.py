"""
Contains all of the views for the Payments app.
"""
# standard library

# third-party
import stripe

# Django
from django.conf import settings
# from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View

# local Django
from . import models


class MembershipPayment(View):
    """
    View meant for displaying pages related to memberships.
    """

    def get(self, request):
        """
        This view renders a page in which users can get more information about
        becoming a member of ACM.

        :param request: Request object that contains information from the
                        user's POST/GET request.
        :type request: :class:`~django.http.request.HttpRequest`

        :returns: An html page which displays the Membership page.
        :rtype: `django.shortcuts.render`
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
    """
    View meant for handling requests related to products & transactions.
    """

    def post(self, request, pk):
        """
        This view submits a Stripe transaction to the database.

        :param request: Request object that contains information from the
                        user's POST/GET request.
        :type request: :class:`~django.http.request.HttpRequest`

        :returns: Html page redirection to the index page or the 404 error page
                  (if the user was authenticated).
        :rtype: :class:`~django.http.HttpResponseRedirect`

        :raises ValueError: If the stripe token is empty or if the stripe
                               api key is invalid.
        :raises django.http.Http404: If an unauthenticated user attempts to
                                     access the page.
        """
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

        product = get_object_or_404(models.Product, pk=pk)
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
