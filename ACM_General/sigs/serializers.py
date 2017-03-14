from rest_framework import serializers
from . import models


class SIGSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SIG
        fields = '__all__'
