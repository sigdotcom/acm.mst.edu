"""
Custom User authentication backends.
"""
# future
from __future__ import unicode_literals

# local Django
from .models import User


class UserBackend(object):
    """
    Authencation backend which authenticates based on a user's email. Used as
    the main authentication method.
    """

    def authenticate(self, request, email=None):
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
        Checks for whether a user is active or not.  This function allows for
        users to be 'shut off' as opposed to deleted, forcing less clean-up and
        increased fidelity when user leaves.

        :param user: :class:`~accounts.models.User` object passed in for
                     authentication.
        :type user: :class:`~accounts.models.User`

        :return: True if the user has the is_active flag set.
                 Flase if the user's is_active flag is false.
        :rtype: bool
        """

        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        """
        Fetches the user from the database whose id (UUID) matches the given
        user_id.

        :param user_id: The UUID for which to find a user for.
        :type user_id: str

        :return: The :class:`~accounts.models.User` object posessing the UUID
                 or None if the UUID does not exist within the database.
        :rtype: :class:`~accounts.models.User`
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
