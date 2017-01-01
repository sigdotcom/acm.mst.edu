import django_filters
from accounts.models import User

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
