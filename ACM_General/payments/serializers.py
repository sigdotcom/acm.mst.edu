"""
Serializers utilized by ``rest_api`` to clean JSON into the various Payments
models.
"""
# third-party
from rest_framework import serializers

# local Django
from . import models


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TransactionCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'
