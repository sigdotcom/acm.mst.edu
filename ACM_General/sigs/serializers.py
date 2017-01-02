from rest_framework import serializers
from sigs.models import SIG 

class SIGSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIG 
        fields = '__all__'
