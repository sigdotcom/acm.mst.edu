"""
Contains the urls for the route ``/social-auth/``.
"""
# Django
from django.conf.urls import url

# local Django
from . import views

app_name = 'thirdparty_auth'
urlpatterns = [
    url(
        r'google/$',
        views.GoogleAuthorization.as_view(),
        name='google'
    ),
    url(
        r'google/callback/$',
        views.GoogleCallback.as_view(),
        name='google-callback'
    ),
]
