"""
Contains urls for the path ``/events/``.
"""
# Django
from django.urls import path

# local Django
from events import views


app_name = 'events'
urlpatterns = [
    # acm.mst.edu/events/
    path('', views.list_events, name='events-list'),

    # acm.mst.edu/events/create/
    path('create/', views.create_event, name='create-event'),
]
