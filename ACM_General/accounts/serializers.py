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
        Ensure the domain of the email is mst.edu.

        :param email: The provided email.
        :type email: String
        :rtype: Boolean
        :return: True if the email has a domain of mst.edu,
                 otherwise Error. 
        """

        if is_valid_email(email):
            return email
        else:
            raise serializers.ValidationError("UserSerializer was passed an "
                                              " invalid email.")

    def create(self, validated_data):
        """
        Create and return an instance of the User model designated by the
        validated_data if no ValidationErrors were raised.

        :param validated_data: Data used for the creation of a new 
                               User instance..
        :type validated_data: Dictionary (?)
        :rtype: User 
        :return: An instance of the User model defined by validated_data.
        """

        return models.User.objects.create(**validated_data)
