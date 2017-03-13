from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from django.shortcuts import render, get_object_or_404
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


class ProductHandler(View):
    def post(self, request, pk):
        """
        TODO: Docstring
        """

        token = request.POST['stripeToken']
        product = get_object_or_404(models.Transaction, pk=pk)
        charge = stripe.Charge.create(
                    currency="usd",
                    amount=product.cost,
                    description=product.description,
                    source=token,
                )

        trans = models.Transaction.objects.create_transaction(
                                        token, user = request.user,
                                        cost = product.cost,
                                        category = 'ACM Membership (Year)',
                                        description = 'See Category',
                                    )

        return HttpResponse(trans)

