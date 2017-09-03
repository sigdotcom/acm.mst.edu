import django_filters
from accounts.models import User
from events.models import Event
from sigs.models import SIG


class UserFilter(django_filters.FilterSet):
    """
    @Desc: Allows for Users to be filtered based on specified
           filtering options.
    """
    class Meta:
        """
        @Desc: Defines for which model and fields the filter set
               applies to. Generates filters for the id, email,
               is_active, is_superuser, and last_login User fields.
        """
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
    """
    @Desc: Allows for Events to be filtered based on specified
           filtering options.
    """
    class Meta:
        """
        @Desc: Defines for which model and fields the filter set
               applies to. Generates filters for all Event fields.
        """
        model = Event
        fields = '__all__'


class SIGFilter(django_filters.FilterSet):
    """
    @Desc: Allows for SIGs to be filtered based on specified 
           filtering options.
    """
    class Meta:
        """
        @Desc: Defines for which model and fields the filter set
               applies to. Generates filters for all SIG fields.
        """
        model = SIG
        fields = '__all__'
