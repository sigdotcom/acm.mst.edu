"""
Contains urls for the ``/accounts/`` route.
"""
# Django
from django.conf.urls import url

# local Django
from . import views

app_name = 'accounts'
urlpatterns = [
    # acm.mst.edu/accounts/logout/
    url(r'logout/', views.user_logout, name='user-logout'),
]
