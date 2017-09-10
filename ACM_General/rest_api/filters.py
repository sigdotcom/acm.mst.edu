# third-party
import django_filters

# local Django
from accounts.models import User
from events.models import Event
from sigs.models import SIG


class UserFilter(django_filters.FilterSet):
    """
    Allows for Users to be filtered based on specified
    filtering options.
    """
    class Meta:
        """
        Defines for which model and fields the filter set
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


#TODO: Implement Filter for Events that allows ImageField
'''
class EventFilter(django_filters.FilterSet):
    """
    Allows for Events to be filtered based on specified
    filtering options.
    """
    class Meta:
        """
        Defines for which model and fields the filter set
        applies to. Generates filters for all Event fields.
        """
        model = Event
'''

class SIGFilter(django_filters.FilterSet):
    """
    Allows for SIGs to be filtered based on specified 
    filtering options.
    """
    class Meta:
        """
        Defines for which model and fields the filter set
        applies to. Generates filters for all SIG fields.
        """
        model = SIG
        fields = '__all__'
