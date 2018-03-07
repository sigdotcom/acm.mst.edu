"""
Contains all of the view for the Home app.
"""
# Third-party
import stripe

# Django
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import (
    HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest,
    HttpResponse
)
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.views import View

# local Django
from events.models import Event
import products.models


def index(request):
    """
    Renders the template for the index page. With that is also grabs next
    events, the number of which depends on settings.MAX_HOME_FLIER_COUNT,
    that aren't past expiry.

    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: :class:`~django.http.request.HttpRequest`

    :return: The render template of the index page.
    :rtype: `django.shortcut.render`
    """
    events = Event.objects.filter(
        date_expire__gte=timezone.now()
    ).order_by('date_hosted')

    num_events = len(events)
    if len(events) >= settings.MAX_HOME_FLIER_COUNT:
        events = events[:settings.MAX_HOME_FLIER_COUNT]

    return (
        render(
            request,
            'home/index.html',
            {
                "upcoming_events": events,
                "num_events": num_events
            }
        )
    )


class Sponsors(View):
    def get(self, request):
        """
        Handles a request to see the sponsors page.

        :param request: Request object that contains information from the
                        user's POST/GET request.
        :type request: django.http.request.HttpRequest

        :return: The render template of the sponsors page.
        :rtype: django.shortcut.render
        """
        return (
            render(
                request,
                'home/sponsors.html',
            )
        )


def calendar(request):
    """
    Handles a request to see the calendar page. Updated to redirect to the
    front page.

    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: :class:`~django.http.request.HttpRequest`

    :return: A redirect to the homepage with a ``#calendar`` anchor which will
             automatically put the user's page onto the calendar.
    :rtype: `django.shortcut.redirect`
    """
    return (
        redirect(
            reverse('home:index') + "#calendar",
            permanent=True,
        )
    )


def media(request):
    """
    Handles a request to see the media page.

    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: :class:`django.http.request.HttpRequest`

    :return: The render template of the media page.
    :rtype: `django.shortcut.render`
    """
    return (
        render(
            request,
            'home/media.html',
        )
    )


def officers(request):
    """
    Handles a request to see the officers page.

    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: :class:`django.http.request.HttpRequest`

    :return: The render template of the officers page.
    :rtype: `django.shortcut.render`
    """
    return (
        render(
            request,
            'home/officers.html',
        )
    )


class Membership(LoginRequiredMixin, View):
    def __init__(self):
        self.login_url = reverse("thirdparty_auth:google")
        self.membership_types = {
            "semester": {
                "tag": "membership-semester",
                "delta": timezone.timedelta(weeks=24)
            },
            "year": {
                "tag": "membership-year",
                "delta": timezone.timedelta(weeks=52)
            }
        }

    def get(self, request):
        """
        Handles a request to see the membership page.
        :param request: Request object that contains information from the
                        user's POST/GET request.
        :type request: django.http.request.HttpRequest

        :return: The render template of the officers page.
        :rtype: django.shortcut.render
        """
        return (
            render(
                request,
                'home/membership.html',
                {
                    "stripe_public_key": getattr(
                        settings, "STRIPE_PUB_KEY", ""
                    ),
                },
            )
        )

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseNotFound("Invalid User")

        token = request.POST.get("stripeToken", None)

        if token is None:
            return HttpResponseBadRequest(
                "ProductHandler view did not receive a stripe"
                " token in the POST request."
            )

        stripe.api_key = getattr(settings, 'STRIPE_PRIV_KEY', None)
        if stripe.api_key == "" or not stripe.api_key:
            raise ValueError(
                "Invalid stripe.api_key specified."
            )

        mem_requested = request.POST.get("type", None)
        mem_attributes = self.membership_types.get(mem_requested, None)

        if mem_attributes is None:
            return HttpResponseBadRequest("Invalid membership type specified.")

        product = products.models.Product.objects.get(
            tag=mem_attributes["tag"]
        )

        # This case will only occur if self.membership_types is improperly set
        if product is None:  # pragma: no cover
            return HttpResponse(
                "Unexpected error occurred. The backend returned an invalid "
                "product. Please contact the administrator.",
                status=500
            )

        try:
            charge = stripe.Charge.create(
                currency="usd",
                amount=int(product.cost * 100),
                description=product.description,
                source=token,
            )
        except stripe.error.APIConnectionError as con_err:  # pragma: no cover
            messages.error(
                request,
                'Could not connect to Stripe payment server. Please try again'
                ' later.'
            )
            return HttpResponseRedirect(reverse("home:membership"))
        except stripe.error.CardError as card_err:
            messages.error(
                request,
                'Received a card error from the Stripe payment server.'
            )
            return HttpResponseRedirect(reverse("home:membership"))
        except stripe.error.AuthenticationError as auth_err:
            return HttpResponse(
                "Unexpected error occurred. Invalid Stripe API key specified "
                "by the backend. Please contact the administrator.",
                status=500
            )
        else:
            request.user.update_mem_expiration(mem_attributes["delta"])

        products.models.Transaction.objects.create_transaction(
            token, user=request.user,
            charge_id=charge.id,
            cost=product.cost,
            sig=product.sig,
            category=product.category,
            description=product.description
        )

        messages.success(
            request,
            'Successfully applied ACM Membership to account.'
        )
        return HttpResponseRedirect(reverse("home:index"))


def sigs(request):
    """
    Handles a request to see the sigs page.

    :param request: Request object that contains information from the user's
                    POST/GET request.
    :type request: :class:`~django.http.request.HttpRequest`

    :return: The render template of the sigs page.
    :rtype: `django.shortcut.render`
    """
    return (
        render(
            request,
            'home/sigs.html',
        )
    )
