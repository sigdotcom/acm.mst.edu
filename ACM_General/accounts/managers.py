# Django
from core.actions import is_valid_email
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Interface for database query operations for the User model.

    Allows seemless creation of users and superusers necessary for the default
    implementation of django.
    """

    use_in_migrations = True

    def get_by_natural_key(self, email):
        """
        Allows for a intutive search of the user by
        the user's email. Similary, this can be done by running
        User.objects.get(email=foo); however, this more standarized,
        django approach to this.

        :param email: The email of the user to search for.
        :type email: String
        :rtype: User
        :return: The User who posseses the provided email.
        """
        return self.get(email=email)

    def _create_user(self, email, **extra_fields):
        """
        Base create_user function that creates a user based on fields passed
        into it and returns the user. 

        :param email: The email of the user to create.
        :type email: String
        :param \**extra_fields: Additional fields used to create the user.
                               Items must be a member variable of the class
                               for which the Manage is a part of.
        :rtype: User
        :return: The newly created User with attributes specified 
                 in **extra_fields. If the email provided has not been
                 whitelisted in ENFORCED_DOMAINS, return a ValueError.
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
        Creates a user based of 'default values' that every user
        should adhere at registration.

        :param email: The email of the user to create.
        :type email: String
        :param \**extra_fields: Additional fields used to create the user.
                               Items must be a member variable of the class
                               for which the Manage is a part of.
        :rtype: User
        :return: Returns a User object created by universal
                 'default values'.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        """
        Creates a 'default' superuser which has access to
        the Django admin panel.

        :param email: The email of the user to create.
        :type email: String
        :param \**extra_fields: Additional fields used to create the user.
                               Items must be a member variable of the class
                               for which the Manage is a part of.
        :rtype: User
        :return: User object created by universal 'default values'
                 that posseses access to the Django admin panel.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, **extra_fields)

'''
class PermissionManager(models.Manager):
    """
    TODO: Docstring
    """
    use_in_migrations = True

    def get_by_natural_key(self, perm_code):
        """
        TODO: Docstring
        """
        return self.get(perm_code=perm_code)

    @staticmethod
    def _create_permission(**kwargs):
        """
        TODO: Docstring
        """
        if not kwargs.get('perm_code'):
            raise ValueError('create_permission must be passed the keyword'
                             ' argument \'perm_code\'')
        if not kwargs.get('perm_desc'):
            raise ValueError('create_permission must be passed the keyword'
                             ' argument \'perm_desc\'')

    def create_permission(self, **kwargs):
        """
        TODO: Docstring
        """
        pass


class GroupManager(models.Manager):
    """
    TODO: Docstring
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        """
        TODO: Docstring
        """
        return self.get(name=name)
'''
