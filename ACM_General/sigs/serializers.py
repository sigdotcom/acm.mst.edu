"""
SIG Serializer utilized by ``rest_api`` to clean JSON into a
:class:`sigs.models.SIG` object.
"""
# third-party
from rest_framework import serializers

# local Django
from . import models


class SIGSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SIG
        fields = '__all__'
