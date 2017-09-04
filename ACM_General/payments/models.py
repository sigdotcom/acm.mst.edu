# standard library
import uuid as uuid

# third-party
import stripe

# Django
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# local Django
from . import managers
from accounts.models import User
from sigs.models import SIG


class TransactionCategory(models.Model):
    """
    @Desc: Transaction Category is meant to allow for the easy categorization
           of the different transactions for more specifed queries.
    """
    objects=managers.TransactionCategoryManager()
    id=models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name=models.CharField(
                verbose_name=_('Category Name'),
                help_text=_('The name of the Category'),
                max_length=50,
            )

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    @Desc: The purpose of the Product class is to create a standard 'template'
           which can be input into a transaction model in a standardized way.
           This allows for miscellaneous transactions to still occur but still
           have a good way of dealing with things such as ACM Memberships,
           Sponsorships, etc.
    """
    objects=managers.ProductManager()
    id=models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name=models.CharField(
                verbose_name=_('Product Name'),
                help_text=_('The name of the Product'),
                max_length=50,
                null=False,
            )
    date_created=models.DateTimeField(
                        verbose_name=_('Date Created'),
                        help_text=_('The date in which the transaction'
                                    ' was created'),
                        auto_now_add=True,
                        editable=False,
                  )
    cost=models.DecimalField(
                    verbose_name=_('Transaction Cost'),
                    help_text=_('How much the transaction costed.'),
                    decimal_places=2,
                    max_digits=7,
                    null=False,
            )
    description=models.CharField(
                    verbose_name=_('Transaction Description'),
                    help_text=_('A description of the transaction.'),
                    max_length=500,
                    null=False,
            )
    category=models.ForeignKey(
                    TransactionCategory,
                    on_delete=models.PROTECT,
                    null=False,
               )
    sig=models.ForeignKey(
                    SIG,
                    on_delete=models.PROTECT,
                    null=False,
                )

    def __str__(self):
        return self.name



class Transaction(models.Model):
    """
    @Desc: The Transaction model will act as storage and classification of any
           ACM transaction including but not limited to ACM Memberships,
           Sponsorships, etc.
    """
    objects=managers.TransactionManager()
    id=models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    date_created=models.DateTimeField(
                        verbose_name=_('Date Created'),
                        help_text=_('The date in which the transaction'
                                    ' was created'),
                        auto_now_add=True,
                        editable=False,
                  )
    description=models.CharField(
                    verbose_name=_('Transaction Description'),
                    help_text=_('A description of the transaction.'),
                    max_length=500,
            )
    category=models.ForeignKey(TransactionCategory, on_delete=models.PROTECT)
    sig=models.ForeignKey(SIG, on_delete=models.PROTECT)
    cost=models.DecimalField(
                    verbose_name=_('Transaction Cost'),
                    help_text=_('How much the transaction costed.'),
                    decimal_places=2,
                    max_digits=7,
                    null=False,
            )
    user=models.ForeignKey(
                    User,
                    on_delete=models.SET_NULL,
                    null=True,
                    verbose_name=_('Transaction User'),
                    help_text=_('The user which completed the transaction.'),
            )
    stripe_token=models.CharField(
                    verbose_name=_('Transaction Stripe Token'),
                    help_text=_('The token associated with the stripe payment.'),
                    max_length=50,
            )
    customer_id=models.CharField(
                    verbose_name=_('Transaction Customer ID'),
                    help_text=_('The Customer ID associated with the user.'),
                    max_length=50,
            )
    coupon_id=models.CharField(
                    verbose_name=_('Transaction Stripe Token'),
                    help_text= _('The coupon which the user used in the transaction.'),
                    max_length=50,
                    null=True,
                    blank=True,
            )
    subscription_id=models.CharField(
                    verbose_name=_('Transaction Subscription ID'),
                    help_text=_('The subscription id associated with the charge'),
                    max_length=50,
                    null=True,
                    blank=True,
            )

    @property
    def stripe_data(self):
        return stripe.Charge.retrieve(
                    self.stripe_token,
                    api_key = getattr(settings, 'STRIPE_PRIV_KEY' , None)
                )

    def __str__(self):
        return self.stripe_token
