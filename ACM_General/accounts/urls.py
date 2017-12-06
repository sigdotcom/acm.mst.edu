"""
Contains urls for the ``/accounts/`` route.
"""
# Django
from django.urls import path

# local Django
from . import views

app_name = 'accounts'
urlpatterns = [
    # acm.mst.edu/accounts/logout/
    path('logout/', views.user_logout, name='user-logout'),
]
