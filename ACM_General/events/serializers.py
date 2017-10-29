"""
Event Serializer utilized by ``rest_api`` to clean JSON into a
:class:`events.models.Event` object.
"""

# third-party
from rest_framework import serializers

# local Django
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
