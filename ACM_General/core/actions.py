from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import re


def is_valid_email(email):
    """
    @Desc: Ensures the any email passed into it adheres to the email domains
           specified in the ENFORCED_EMAIL_DOMAINS field in the settings.

    @Returns: If the email is valid, it returns true, otherwise it 
              returns false.
    """
    valid_domains = getattr(settings, 'ENFORCED_EMAIL_DOMAINS', None)

    if valid_domains is None:
        raise ImproperlyConfigured('ENFORCED_EMAIL_DOMAINS must be specified'
                                   'in the Django configuration.')
    for domain in valid_domains:
        if(re.fullmatch(r'.+@'+domain, email)):
                return True

    return False
