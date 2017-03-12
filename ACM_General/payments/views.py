from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from payments.models import Transaction
import stripe

# Create your views here.

stripe.api_key = getattr(settings, 'STRIPE_KEY' , None)

if(stripe.api_key == None):
    raise ImproperlyConfigured('Please enter a Stripe API key into settings_local')


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

        trans = Transation.objects.create_transaction(
                                        token, user = request.user,
                                        cost = amount,
                                        category = 'ACM Membership (Year)',
                                        description = 'See Category',
                                    )

        return HttpResponse(trans)

