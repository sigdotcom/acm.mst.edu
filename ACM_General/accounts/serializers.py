"""
User Serializer utilized by ``rest_api`` to clean JSON into a
:class:`accounts.models.User` object.
"""

# third-party
from rest_framework import serializers

# Django
from core.actions import is_valid_email

# local Django
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ('password', )

    @staticmethod
    def validate_email(email):
        """
        Ensure the domain of the email is within
        :setting:`ENFORCED_EMAIL_DOMAINS`.

        :param email: The email to be validated.
        :type email: str

        :return: True if the email has a domain in
                 :setting:`ENFORCED_EMAIL_DOMAINS`.
        :rtype: bool

        :raises serializers.ValidationError: If the email domain is not located
                                             in
                                             :setting:`ENFORCED_EMAIL_DOMAINS`.
        """

        if is_valid_email(email):
            return email
        else:
            raise serializers.ValidationError("UserSerializer was passed an "
                                              " invalid email.")

    def create(self, validated_data):
        """
        Creates of the :class:`accounts.models.User` based on `validated_data`.

        :param validated_data: Data used for the creation of a new
                               :class:`accounts.models.User` instance.
        :type validated_data: dict

        :return: An instance of the User model defined by validated_data.
        :rtype: :class:`accounts.models.User`
        """

        return models.User.objects.create(**validated_data)
