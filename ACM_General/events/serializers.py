from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    #flier_url = serializers.SerializerMethodField(source='get_flier_url')
    #flier = serializers.ImageField(source='get_flier')
    #flier = serializers.Field('image.url')

    class Meta:
        model = Event
        fields = '__all__'
        #fields = ('id', 'date_created', 'date_hosted', 'date_expire', 'creator', 'hosting_sig',
        #    'title', 'description', 'location', 'presenter', 'cost', 'link', 'flier', 'flier_url')

    #def get_flier(self, obj):
    #    if obj.flier:
    #        return self.context['request'].build_absolute_uri(obj.flier.url)
