from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def isValidEmail(email):
    """
    @Desc: Ensures the any email passed into it adheres to the email domains
           specified in the ENFORCED_EMAIL_DOMAINS field in the settings.

    @Returns: If the email is valid, it returns the email, otherwise it raises
              an error.
    """
    domain = email.split('@')[1]
    valid_domains = getattr(settings, 'ENFORCED_EMAIL_DOMAINS', None)

    if(valid_domains is None):
        raise ImproperlyConfigured('ENFORCED_EMAIL_DOMAINS must be specified'
                                   'in the Django configuration.')
        
    if(domain in valid_domains): 
        return(email)

    raise ValueError('Email domain is invalid. The domain entered was'
                     ' \'{}\' which does not match' 
                     ' ENFORCED_EMAIL_DOMAINS'.format(domain))
