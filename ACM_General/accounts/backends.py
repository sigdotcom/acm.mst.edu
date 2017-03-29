from __future__ import unicode_literals
from .models import User


class UserBackend(object):
    """
    Authencation backend which supports email as USERNAME_FIELD.
    """

    def authenticate(self, email=None):
        """
        @Desc - authenticates whether or not a user is in the database based on
                a given email. Necessary for login as Django requires
                this function to be run on any to-be-logined user.
        """

        ###
        # TODO: Find a better way to throw error at no email
        ###

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if self.user_can_authenticate(user):
                return user
            else:
                return None

    @staticmethod
    def user_can_authenticate(user):
        """
        @Desc - Returns true if the user has the is_active flag set. This
                function allows for users to be 'shut off' of opposed to
                deleted, forcing less clean-up and increased fidelity when user
                leaves. If is_active is false, returns False.
        """

        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        """
        @Desc - Fetches the user from the database whose id (UUID) matches the
                given user_id; otherwise, returns None.
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
