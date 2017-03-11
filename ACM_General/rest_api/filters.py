import django_filters
from ACM_General.accounts.models import User
from ACM_General.events.models import Event
from ACM_General.sigs.models import SIG


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


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = '__all__'


class SIGFilter(django_filters.FilterSet):
    class Meta:
        model = SIG 
        fields = '__all__'
