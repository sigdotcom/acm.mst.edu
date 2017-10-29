"""
Location for various general use functions which may be useful in a variety of
applications.
"""

# standard library
import re

# Django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def is_valid_email(email):
    """
    Ensures the any email passed into it adheres to the email domains
    specified in the ``ENFORCED_EMAIL_DOMAINS`` field in the settings.

    :param email: The email to be validated.
    :type email: str

    :return: If the email is valid, it returns `True`, otherwise it
             returns `False`.
    :rtype: bool

    :raise ImproperlyConfigured: Raises when encountering an invalid email.
    """
    valid_domains = getattr(settings, 'ENFORCED_EMAIL_DOMAINS', None)

    if valid_domains is None:
        raise ImproperlyConfigured('ENFORCED_EMAIL_DOMAINS must be specified'
                                   'in the Django configuration.')
    for domain in valid_domains:
        if re.fullmatch(r'.+\..+', domain) is None:
            raise ImproperlyConfigured('Emails much match the pattern foo.foo')
        if(re.fullmatch(r'.+@' + domain, email)):
            return True

    return False
