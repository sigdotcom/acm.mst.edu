from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from django.conf import settings
from accounts.models import User



class UserBackend(object):
    """
    Authencation backend which supports email as USERNAME_FIELD.
    """

    def authenticate(self, email=None, **kwargs):
        """
        Authenticates whether an email and password passed to it is registered
        in the database.
        """

        ###
        # TODO: Find a better way to throw error at no email
        ###
        user = None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if(self.user_can_authenticate(user)):
                return user

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't 
        have that attribute are allowed.
        """

        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        """
        Returns the user instance identified by user_id
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
