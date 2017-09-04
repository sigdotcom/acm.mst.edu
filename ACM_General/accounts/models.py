# future
from __future__ import unicode_literals

# standard library
import uuid as uuid

# Django
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local Django
from . import managers


class User(AbstractBaseUser):
    """
     @Desc - Overloading of the base user class to enable email validation
             as apposed to username validation in default django
     @Fields -
      id - 16 character UUID which uniquely identifies each user
      email - Stores the user's email
      date_joined - Stores when the user signs up
      is_active - Whether or not a user accoutn should be considered 'active'
      is_admin - Stores whether or not the user can access the admin panel
      objects - Container for the User Manager
    """
    ##
    # TODO: Integrations.
    ##

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    email = models.EmailField(
                verbose_name=_('Email Address'),
                help_text=_('A valid @mst.edu email address'),
                unique=True,
                db_index=True,
            )
    first_name = models.CharField(
                        verbose_name=_('First Name'),
                        max_length=30,
                 )

    last_name = models.CharField(
                        verbose_name=_('Last Name'),
                        max_length=30,
                )
    date_joined = models.DateTimeField(
                        verbose_name=_('Date Joined'),
                        auto_now_add=True,
                        editable=False,
                  )
    is_active = models.BooleanField(
                        verbose_name=_('Is Active'),
                        default=True,
                )
    is_staff = models.BooleanField(
                        verbose_name=_('Is Staff'),
                        default=False,
               )
    is_superuser = models.BooleanField(
                        verbose_name=_('Is Superuser'),
                        default=False,
                   )

    @property
    def is_admin(self):
        return self.is_superuser

    def get_full_name(self):
        """
        @Returns: The user's full name
        """
        return str(self.first_name) + " " + str(self.last_name)

    def get_short_name(self):
        """
        @Returns: The user's email
        """
        return self.email

    def __str__(self):
        """
        @Returns: The user's email
        """
        return self.email
