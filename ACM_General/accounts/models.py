"""
Contains User model which encapsulates each website 'User'.
"""

# future
from __future__ import unicode_literals

# standard library
import uuid as uuid

# Django
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# local Django
from . import managers


class User(AbstractBaseUser):
    """
    Overloading of the base user class to enable email validation
    as opposed to username validation in default django.
    """
    #: Container for the User Manager.
    objects = managers.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    #: 16 character UUID which uniquely identifies each user.
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)

    #: Stores the user's email.
    email = models.EmailField(
        verbose_name=_('Email Address'),
        help_text=_('A valid @mst.edu email address'),
        unique=True,
        db_index=True,
    )
    #: Stores the user's first name.
    first_name = models.CharField(
        verbose_name=_('First Name'),
        max_length=30,
    )
    #: Stores the user's last name.
    last_name = models.CharField(
        verbose_name=_('Last Name'),
        max_length=30,
    )
    #: Stores when the user signs up.
    date_joined = models.DateTimeField(
        verbose_name=_('Date Joined'),
        auto_now_add=True,
        editable=False,
    )

    #: Stores when the user's ACM Membership will expire; represented as a
    #: DateTimeField.
    membership_expiration = models.DateTimeField(
        verbose_name=_('Membership Expiration Date'),
        null=True
    )

    #: Whether or not a user account should be considered 'active'.
    is_active = models.BooleanField(
        verbose_name=_('Is Active'),
        default=True,
    )
    #: Stores whether or not the user is staff.
    is_staff = models.BooleanField(
        verbose_name=_('Is Staff'),
        default=False,
    )
    #: Stores whether or not the user can access the admin panel.
    is_superuser = models.BooleanField(
        verbose_name=_('Is Superuser'),
        default=False,
    )

    @property
    def is_admin(self):
        """
        Returns the user's admin status

        :return: The user's admin status
        :rtype: bool
        """
        return self.is_superuser

    @property
    def is_member(self):
        """
        Whether or not a user is an ACM member

        :return: The user's current membership status
        :rtype: bool
        """
        expiration_date = self.membership_expiration

        if expiration_date is not None:
            return timezone.now() <= expiration_date
        else:
            return False

    def update_mem_expiration(self, time_delta):
        """
        Update the user's ACM expiration date to a new time_delta

        :param time_delta: The amount of time to increase the membership
                           expiration date.
        :type time_delta: django.utils.timezone.timedelta

        .. note::
            This operation saves the user every time it is applied. This may
            result in a performance bottleneck later, but the saving should
            be a default action when applying this operation.
        """
        if not self.is_member:
            self.membership_expiration = timezone.now() + time_delta
        else:
            self.membership_expiration += time_delta

        self.save()

    def get_full_name(self):
        """
        Returns the user's full name.

        :return: The user's full name.
        :rtype: str
        """
        return str(self.first_name) + " " + str(self.last_name)

    def get_short_name(self):
        """
        Returns the user's email.

        :return: The user's email.
        :rtype: str
        """
        return self.email

    def __str__(self):
        """
        Returns the user's email.

        :return: The user's email.
        :rtype: str
        """
        return self.email
