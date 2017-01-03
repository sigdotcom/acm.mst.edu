from rest_framework import serializers
from core.actions import isValidEmail
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
        )
    def validate_email(self, email):
        """
        Ensure the domain of the email is mst.edu
        """

        email = isValidEmail(email)

        return(email)

    def create(self, validated_data):
        """
        Create and return an instance of the User model designated by the
        validated_data if no ValidationErrors were raised
        """

        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update the data of an exsisting User model with the validated_data
        provided in the request if no ValidationError was raised
        """

        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', 
                                                 instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', 
                                                    instance.is_superuser)
        instance.save()
        return(instance)

