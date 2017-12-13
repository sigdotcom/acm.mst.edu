"""
Contains the urls for the route ``/social-auth/``.
"""
# Django
from django.urls import path

# local Django
from . import views

app_name = 'thirdparty_auth'
urlpatterns = [
    path(
        'google/',
        views.GoogleAuthorization.as_view(),
        name='google'
    ),
    path(
        'google/callback/',
        views.GoogleCallback.as_view(),
        name='google-callback'
    ),
]
