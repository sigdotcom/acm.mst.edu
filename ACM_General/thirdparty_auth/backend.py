from django.conf import settings
from accounts.models import User

class GoogleOAuth2Backend(object):
    def authenticate(self, token=None):
        pass

    def get_user(self, token):
        pass
