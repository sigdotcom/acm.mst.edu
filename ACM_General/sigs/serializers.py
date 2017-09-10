# third-party
from rest_framework import serializers

# local Django
from . import models


class SIGSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SIG
        fields = '__all__'
