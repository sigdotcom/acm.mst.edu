"""
Contains all of the routes for ``/``.
"""
# Django
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

# local Django
from . import views

app_name = "home"
urlpatterns = [
    # https://acm.mst.edu/
    url(r'^$', views.index, name="index"),
    # https://acm.mst.edu/calendar/
    url(r'^calendar/$', views.calendar, name="calendar"),
    # https://acm.mst.edu/media/
    url(r'^media/$', views.media, name="media"),
    # https://acm.mst.edu/membership/
    url(r'^membership/$', views.membership, name="membership"),
    # https://acm.mst.edu/officers/
    url(r'^officers/$', views.officers, name="officers"),
    # https://acm.mst.edu/sigs/
    url(r'^sigs/$', views.sigs, name="sigs"),
    # https://acm.mst.edu/sponsors/
    url(r'^sponsors/$', views.sponsors, name="sponsors"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
