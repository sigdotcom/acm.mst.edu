"""
UserManager class and helper functions. Allows for serialized ``create_user``
which properly validates the input as well as getting a user by email.
"""
# Django
from core.actions import is_valid_email
from django.contrib.auth.base_user import BaseUserManager
# Will be used if other managers return
# from django.db import models


class UserManager(BaseUserManager):
    """
    Interface for database query operations for the
    :class:`~accounts.models.User` model.

    Allows seamless creation of users and superusers necessary for the default
    implementation of Django.
    """

    use_in_migrations = True

    def get_by_natural_key(self, email):
        """
        Allows for a intuitive search of the user by
        the user's email. Similarly, this can be done by running
        ``User.objects.get(email=foo)``; however, this is a more standardized,
        Django approach to this.

        :param email: The email of the user to search for.
        :type email: str

        :return: The User who posseses the provided email.
        :rtype: :class:`~~accounts.models.User`
        """
        return self.get(email=email)

    def _create_user(self, email, **extra_fields):
        """
        Base ``create_user`` function that creates a user based on fields passed
        into it.

        :param email: The email of the user to create.
        :type email: str
        :param \**extra_fields: Additional fields used to create the user.
                                Items must be a member variable of the class
                                for which the Manage is a part of.

        :return: The newly created User with attributes specified
                 in \**extra_fields. If the email provided has not been
                 whitelisted in ENFORCED_DOMAINS, return a ValueError.
        :rtype: :class:`~accounts.models.User`
        """
        if(is_valid_email(email)):
            email = self.normalize_email(email)
            user = self.model(email=email,
                              **extra_fields)
            user.set_unusable_password()
            user.save(using=self._db)

            return user
        else:
            raise ValueError('create_user() was supplied an email not'
                             ' whitelisted in ENFORCED_DOMAINS. See'
                             ' settings.py.')

    def create_user(self, email, **extra_fields):
        """
        Creates a user based off 'default values' that every user
        should adhere at registration.

        :param email: The email of the user to create.
        :type email: str
        :param \**extra_fields: Additional fields used to create the user.
                               Items must be a member variable of the class
                               for which the Manage is a part of.

        :return: Returns a User object created by universal
                 'default values'.
        :rtype: :class:`~accounts.models.User`
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        """
        Creates a 'default' superuser.

        :param email: The email of the user to create.
        :type email: str
        :param \**extra_fields: Additional fields used to create the user.
                                Items must be a member variable of the class
                                for which the Manage is a part of.

        :return: User object created by universal 'default values'
                 that posseses access to the Django admin panel.
        :rtype: :class:`~accounts.models.User`
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, **extra_fields)
