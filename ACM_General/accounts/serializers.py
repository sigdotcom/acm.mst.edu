from rest_framework import serializers
from ACM_General.core.actions import is_valid_email
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ('password', )

    @staticmethod
    def validate_email(email):
        """
        Ensure the domain of the email is mst.edu
        """

        email = is_valid_email(email)

        return email

    def create(self, validated_data):
        """
        Create and return an instance of the User model designated by the
        validated_data if no ValidationErrors were raised
        """

        return models.User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update the data of an exsisting User model with the validated_data
        provided in the request if no ValidationError was raised
        """

        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
