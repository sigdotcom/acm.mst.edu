###
# Default Django Imports
###
from __future__ import unicode_literals

from django.db import models

###
# Custom Django Imports
###
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

import uuid

# Create your models here.

class AbstractBaseUserManager(BaseUserManager):
    """
    Interface for database query operations for the User model.

    Allows seemless creation of users and superusers necessary for the default 
    implementation of django.
    """
    
    def _create_user(self, email, **extra_fields):
        """
        Base create_user function that creates a user based on fields passed 
        into it and returns the user.  extra_fields must be a member variable
        of the class which the Manager is apart of.
        """

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          **extra_fields)
        self.set_unusable_password()
        user.save(using=self._db)

        return user

    def create_user(self, email, **extra_fields):
        """
        create_user creates a user based of 'default values' that every user
        should adhere at registration.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        """
        create_superuser creates a 'default' superuser which has access to
        the django admin panel.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
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
    email = models.EmailField('email address', 
                              unique=True, 
                              db_index = True, 
                              null=True)
    date_joined = models.DateTimeField(auto_now_add = True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = AbstractBaseUserManager() 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_short_name(self):
        """
        get_short_name returns the user's email when this method is called
        upon the class.
        """
        return(self.email)

    def __unicode__(self):
        """
        __unicode__ returns the user's email when unicode() is run on the 
        User class.
        """
        return(self.email)

    def __str__(self):
        """
        __str__ returns the user's email when str() is run on the User class
        return self.email.
        """
        return(self.email)

