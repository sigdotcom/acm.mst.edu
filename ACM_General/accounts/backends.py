"""
Custom User authentication backends.
"""
# future
from __future__ import unicode_literals

# local Django
from django.contrib.auth import get_user_model
from django.contrib.auth import backends
from .models import User

UserModel = get_user_model()


class UserBackend(backends.ModelBackend):
    """
    Authencation backend which authenticates based on a user's email. Used as
    the main authentication method.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticates whether or not a user is in the database based on a given
        email. Necessary for login as Django requires this function to be run
        on any to-be-logged-in user.

        :param email: :class:`~accounts.models.User` provided email address.
        :type email: str

        :return: The :class:`~accounts.models.User` object posessing the given
                 email, or None if the email does not exist within the
                 database.
        :rtype: :class:`~accounts.models.User` or None
        """
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except User.DoesNotExist:
            return None
        else:
            if self.user_can_authenticate(user):
                return user

            return None
