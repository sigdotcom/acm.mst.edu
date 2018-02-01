"""
Defines the app name for the rest_api app.
"""
# future
from __future__ import unicode_literals

# Django
from django.apps import AppConfig


class RestApiConfig(AppConfig):
    """
    Defines a global app name for the rest_api app.
    """
    name = 'rest_api'
