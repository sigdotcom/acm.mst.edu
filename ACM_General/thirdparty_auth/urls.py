# Django
from django.conf.urls import url

# local Django
from . import views

app_name = 'thirdparty_auth'
urlpatterns = [
    url(
        r'^(?P<auth_type>[0-9a-z-]+)/(?P<auth_provider>[0-9a-z-]+)/$',
        views.AuthorizationView.as_view(),
        name='login'
    ),
    url(
        r'^(?P<auth_type>[0-9a-z-]+)/(?P<auth_provider>[0-9a-z-]+)/callback/$',
        views.TokenView.as_view(),
        name='callback'
    ),
]
