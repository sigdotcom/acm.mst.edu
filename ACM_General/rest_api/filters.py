import django_filters
from accounts.models import User
from events.models import Event
from sigs.models import SIG


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login'
        ]


#TODO: Implement Filter for Events that allows ImageField
'''
class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
'''

class SIGFilter(django_filters.FilterSet):
    class Meta:
        model = SIG
        fields = '__all__'
