# Django
from django.conf.urls import url
# from django.conf.urls import include

# local Django
from events import views


app_name = 'events'
urlpatterns = [
    # acm.mst.edu/events/
    url('^$', views.list_events, name='events-list'),

    # acm.mst.edu/events/create/
    url('create/$', views.create_event, name='create-event'),
]
