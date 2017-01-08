###
# Default Django Imports
###
from __future__ import unicode_literals

from django.db import models

###
# Custom Django Imports
###
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from core.actions import isValidEmail
from accounts import managers

import uuid

# Create your models here.
class Permission(models.Model):
    perm_code = models.CharField(
                        verbose_name = _('Permission Code'),
                        help_text = _('In-code reference to the permission'
                                      ' title.'),
                        max_length = 20,
                        unique = True,
                )
    perm_desc = models.CharField(
                        verbose_name = _('Permission Description'),
                        help_text = _('A description of what the permission'
                                      ' gives the User access to.'),
                        max_length = 500,
                )

class Group(models.Model):
    permissions = models.ManyToManyField(
                            Permission,
                            verbose_name = _('Group Permissions'),
                            help_text = _('The permissions related to the'
                                          ' specific group'),
                  )
    group_name = models.CharField(
                        verbose_name = _('Group Name'),
                        help_text = _('The name of the Permissions group'),
                        max_length = 20,
                        blank = False,
                 )
    group_description = models.CharField(
                                verbose_name = _('Group Description'),
                                help_text = _('The description of the Group'),
                                max_length = 500,
                        )

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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
                verbose_name = _('Email Address'),
                unique=True,
                db_index = True,
                null = True,
                help_text= _('A valid @mst.edu email address'),
            )
    first_name = models.CharField(
                        verbose_name = _('First Name'),
                        max_length=30,
                        blank=True,
                 )

    last_name = models.CharField(
                        verbose_name = _('Last Name'),
                        max_length = 30,
                        blank = True,
                )
    date_joined = models.DateTimeField(
                        verbose_name = _('Date Joined'),
                        auto_now_add = True,
                        editable=False,
                  )
    is_active = models.BooleanField(
                        verbose_name= _('Is Active'),
                        default=True,
                )
    is_staff = models.BooleanField(
                        verbose_name= _('Is Staff'),
                        default=False,
               )
    is_superuser = models.BooleanField(
                        verbose_name= _('Is Superuser'),
                        default=False,
                   )
    objects = managers.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_admin(self):
        return(self.is_superuser)

    def get_full_name(self):
        """
        @Returns: The user's full name
        """
        return(str(self.first_name) + " " + str(self.last_name))

    def get_short_name(self):
        """
        @Returns: The user's email
        """
        return(self.email)

    def __unicode__(self):
        """
        @Returns: The user's email
        """
        return(self.email)

    def __str__(self):
        """
        @Returns: The user's email
        """
        return(self.email)


