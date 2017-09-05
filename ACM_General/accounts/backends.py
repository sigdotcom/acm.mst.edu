# future
from __future__ import unicode_literals

# local Django
from .models import User


class UserBackend(object):
    """
    Authencation backend which supports email as USERNAME_FIELD.
    """

    def authenticate(self, email=None):
        """
        Authenticates whether or not a user is in the database based on
        a given email. Necessary for login as Django requires
        this function to be run on any to-be-logined user.

        :param email: User provided email address.
        :type email: String
        :rtype: User
        :return: The User object posessing the given email, or None
                 if the email does not exist within the database.
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
        Checks for whether a user is active or not.
        This function allows for users to be 'shut off' of opposed to
        deleted, forcing less clean-up and increased fidelity when user
        leaves.

        :param user: User object passed in for authentication.
        :type user: User 
        :rtype: Boolean
        :return: True if the user has the is_active flag set.
                 Flase if the user's is_active flag is false.
        """

        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        """
        Fetches the user from the database whose id (UUID) matches the
        given user_id.

        :param user_id: The UUID for which to find a user for. 
        :type user_id: String 
        :rtype: User
        :return: The User object posessing the UUID or None, if the
                 UUID does not exist withing the database.
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
