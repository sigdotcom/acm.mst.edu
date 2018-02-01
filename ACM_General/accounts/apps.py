"""
Defines the app name for the accounts app.
"""

# future
from __future__ import unicode_literals

# Django
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Defines a global app name for the accounts app.
    """
    name = 'accounts'
