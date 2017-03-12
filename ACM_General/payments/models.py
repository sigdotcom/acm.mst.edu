from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from accounts.models import User
from payments import managers

# Create your models here.

class Transaction(models.Model):
    """
    TODO: Add Transaction Docstring
    """

    objects = managers.TransactionManager()

    trans_types = (
            ('ACM Membership (Semester)', 'ACM Membership (Semester)'),
            ('ACM Membership (Year)', 'ACM Membership (Year)'),
            ('Sponsor', 'Sponsorship'),
    )

    date_joined = models.DateTimeField(
                        verbose_name = _('Date Joined'),
                        auto_now_add = True,
                        editable=False,
                  )
    category = models.CharField(
                    verbose_name = _('Transaction Type'),
                    help_text = _('The type of transaction which occured'),
                    max_length = 50,
                    choices = trans_types,
            )
    description = models.CharField(
                    verbose_name = _('Transaction Description'),
                    help_text = _('A description of the transaction.'),
                    max_length = 500,
            )
    cost = models.DecimalField(
                    verbose_name = _('Transaction Cost'),
                    help_text = _('How much the transaction costed.'),
                    decimal_places = 2,
                    max_digits = 7,
                    null = False,
            )
    user = models.ForeignKey(
                    User,
                    on_delete=models.SET_NULL,
                    null=True,
                    verbose_name = _('Transaction User'),
                    help_text = _('The user which completed the transaction.'),
            )
    stripe_token = models.CharField(
                    verbose_name = _('Transaction Stripe Token'),
                    help_text= _('The token associated with the stripe payment.'),
                    max_length=25,
            )
    customer_id = models.CharField(
                    verbose_name = _('Transaction Customer ID'),
                    help_text= _('The Customer ID associated with the user.'),
                    max_length=25,
            )
    coupon_id = models.CharField(
                    verbose_name = _('Transaction Stripe Token'),
                    help_text= _('The coupon which the user used in the transaction.'),
                    max_length=25,
                    null=True,
                    blank=True,
            )
    subscription_id = models.CharField(
                    verbose_name = _('Transaction Subscription ID'),
                    help_text = _('The subscription id associated with the charge'),
                    max_length=25,
                    null=True,
                    blank=True,
            )

    def __unicode__(self):
        return self.customer_id

    def __str__(self):
        return self.customer_id

