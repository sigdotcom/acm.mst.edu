"""
Contains all of the view for the Home app.
"""
# Django
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.conf import settings
from django.views import View

# local Django
from events.models import Event


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

    if len(events) >= settings.MAX_HOME_FLIER_COUNT:
        events = events[:settings.MAX_HOME_FLIER_COUNT]

    return (
        render(
            request,
            'home/index.html',
            {"upcoming_events": events}
        )
    )


class Sponsors(View):
    def get(self, request):
        """
        Handles a request to see the sponsors page.

        :param request: Request object that contains information from the user's
                        POST/GET request.
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

    def post(self, request):
        if not request.user.is_authenticated():
            raise Http404("Invalid User")

        token = request.POST.get("stripeToken", None)
        membership_type = request.POST.get("type", None)
        if token is None:
            raise ValueError(
                "ProductHandler view did not receive a stripe"
                " token in the POST request."
            )

        stripe.api_key = getattr(settings, 'STRIPE_PRIV_KEY', None)
        if stripe.api_key == "" or not stripe.api_key:
            raise ValueError(
                "ProductHandler view has an invalid"
                " stripe.api_key, please insert one in"
                " settings_local.py."
            )

        stripe.Charge.create(
            currency="usd",
            amount=int(self.product.cost * 100),
            description=product.description,
            source=token,
        )

        models.Transaction.objects.create_transaction(
            token, user=request.user,
            cost=self.product.cost,
            sig=self.product.sig,
            category=self.product.category,
            description=self.product.description
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


class Membership(View):
    def get(self, request):
        """
        Handles a request to see the membership page.
        :param request: Request object that contains information from the user's
                        POST/GET request.
        :type request: django.http.request.HttpRequest

        :return: The render template of the officers page.
        :rtype: django.shortcut.render
        """
        return (
            render(
                request,
                'home/membership.html',
                {
                    "stripe_public_key": getattr(settings, "STRIPE_PUB_KEY", "")
                },
            )
        )

    def post(self, request):
        if not request.user.is_authenticated():
            raise Http404("Invalid User")

        token = request.POST.get("stripeToken", None)
        membership_type = request.POST.get("type", None)
        if token is None:
            raise ValueError(
                "ProductHandler view did not receive a stripe"
                " token in the POST request."
            )

        stripe.api_key = getattr(settings, 'STRIPE_PRIV_KEY', None)
        if stripe.api_key == "" or not stripe.api_key:
            raise ValueError(
                "ProductHandler view has an invalid"
                " stripe.api_key, please insert one in"
                " settings_local.py."
            )

        stripe.Charge.create(
            currency="usd",
            amount=int(self.product.cost * 100),
            description=product.description,
            source=token,
        )

        models.Transaction.objects.create_transaction(
            token, user=request.user,
            cost=self.product.cost,
            sig=self.product.sig,
            category=self.product.category,
            description=self.product.description
        )


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
