"""
Contains urls for the path ``/events/``.
"""
# Django
from django.conf import settings
from django.conf.urls import url
# from django.conf.urls import include
from django.conf.urls.static import static

# local Django
from events import views


app_name = 'events'
urlpatterns = [
    # acm.mst.edu/events/
    url('^$', views.list_events, name='events-list'),

    # acm.mst.edu/events/create/
    url('create/$', views.create_event, name='create-event'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
