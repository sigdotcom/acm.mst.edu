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
    Transaction Category is meant to allow for the easy categorization of the
    different transactions for more specific queries.
    """
    objects = managers.TransactionCategoryManager()

    #: The id of the TransactionCategory; represented as a UUIDField.
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid1,
        editable=False
    )

    #: The name of the Category; represented as a CharField.
    name = models.CharField(
        verbose_name=_('Category Name'),
        help_text=_('The name of the Category'),
        max_length=50,
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The purpose of the Product class is to create a standard 'template' which
    can be input into a transaction model in a standardized way. This allows
    for miscellaneous transactions to still occur but still have a good way of
    dealing with things such as ACM Memberships, Sponsorships, etc.
    """
    objects = managers.ProductManager()

    #: The id of the Product; represented as a UUIDField.
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)

    #: The name of the Product; represented as CharField.
    name = models.CharField(
        verbose_name=_('Product Name'),
        help_text=_('The name of the Product'),
        max_length=50,
        null=False,
    )

    #: The date in which the transaction was created; represented as a
    #: DateTimeField.
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        help_text=_('The date in which the transaction was created'),
        auto_now_add=True,
        editable=False,
    )

    #: The cost of the transaction; represented as a DecimalField.
    cost = models.DecimalField(
        verbose_name=_('Transaction Cost'),
        help_text=_('How much the transaction costed.'),
        decimal_places=2,
        max_digits=7,
        null=False,
    )

    #: A description of the transaction; represented as a CharField.
    description = models.CharField(
        verbose_name=_('Transaction Description'),
        help_text=_('A description of the transaction.'),
        max_length=500,
        null=False,
    )

    #: The category of the type of transaction; represented as ForeignKey of
    #: the TransactionCategory model.
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.PROTECT,
        null=False,
        help_text=_('The category of the type of transaction.'),
    )

    #: The SIG to whom the Product is related to; represented as a ForeignKey
    #: of the SIG model.
    sig = models.ForeignKey(
        SIG,
        on_delete=models.PROTECT,
        null=False,
        help_text=_('The SIG to whom the Product is related to.')
    )

    def __str__(self):
        return self.name



class Transaction(models.Model):
    """
    The Transaction model will act as storage and classification of any ACM
    transaction including but not limited to ACM Memberships, Sponsorships,
    etc.
    """
    objects = managers.TransactionManager()

    #: The id of the Transaction; represented as a UUIDField.
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)

    #: The date in which the transaction was created; represented as a
    #: DateTimeField.
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        help_text=_('The date in which the transaction was created.'),
        auto_now_add=True,
        editable=False,
    )

    #: A description of the transaction; represented as a CharField.
    description = models.CharField(
        verbose_name=_('Transaction Description'),
        help_text=_('A description of the transaction.'),
        max_length=500,
    )

    #: The category of the Transaction; represented as a ForeignKey of the
    #: TransactionCategory model.
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.PROTECT
    )

    #: The SIG to whom the Transaction is for; represented as a ForeignKey of
    #: the SIG model.
    sig = models.ForeignKey(
        SIG,
        on_delete=models.PROTECT
    )

    #: How much the transaction costed; represented as a DecimalField.
    cost = models.DecimalField(
        verbose_name=_('Transaction Cost'),
        help_text=_('How much the transaction costed.'),
        decimal_places=2,
        max_digits=7,
        null=False,
    )

    #: The user which completed the transaction; represented as a ForeignKey of
    #: the User model.
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Transaction User'),
        help_text=_('The user which completed the transaction.'),
    )

    #: The token associated with the stripe payment; represented as a
    #: CharField.
    stripe_token = models.CharField(
        verbose_name=_('Transaction Stripe Token'),
        help_text=_('The token associated with the stripe payment.'),
        max_length=50,
    )

    #: The Customer ID associated with the user; represented as a CharField.
    customer_id = models.CharField(
        verbose_name=_('Transaction Customer ID'),
        help_text=_('The Customer ID associated with the user.'),
        max_length=50,
    )

    #: The coupon which the user used in the transaction; represented as a
    #: CharField.
    coupon_id = models.CharField(
        verbose_name=_('Transaction Stripe Token'),
        help_text= _('The coupon which the user used in the transaction.'),
        max_length=50,
        null=True,
        blank=True,
    )

    #: The subscription id associated with the charge; represented as a
    #: CharField.
    subscription_id = models.CharField(
        verbose_name=_('Transaction Subscription ID'),
        help_text=_('The subscription id associated with the charge.'),
        max_length=50,
        null=True,
        blank=True,
    )

    @property
    def stripe_data(self):
        """
        .. ...................... CONSTANT LINK ...........................
        .. _stripe-charge-link: https://stripe.com/docs/api#retrieve_charge
        .. ................................................................

        Retrieves data related to the stripe charge made. More info `here <stripe-charge-link_>`_.

        :rtype: stripe.Charge
        :returns: A charge if a valid identifier was provided, and raises an
                  error otherwise.
        """
        return stripe.Charge.retrieve(
            self.stripe_token,
            api_key=getattr(settings, 'STRIPE_PRIV_KEY' , None)
        )

    def __str__(self):
        return self.stripe_token
