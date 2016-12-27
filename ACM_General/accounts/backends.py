from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


UserModel = get_user_model()

class UserBackend(object):
    """
    Authencation backend which supports email as USERNAME_FIELD.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticates whether an email and password passed to it is registered
        in the database.
        """

        if(email is None):
            email = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            user = UserModel._default_manager.get_by_natural_key(email)
        except UserModel.DoesNotExist:
            return None
        else:
            if(user.check_password(password) 
               and self.user_can_authenticate(user)):
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
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
