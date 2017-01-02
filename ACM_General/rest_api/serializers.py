from rest_framework import serializers
from accounts.models import Event 

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event 
        fields = '__all__'
