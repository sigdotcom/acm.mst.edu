"""
Contains all of the routes for ``/``.
"""
# Django
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.http import HttpResponse


# local Django
from . import views

app_name = "home"
urlpatterns = [
    path('robots.txt', lambda x: HttpResponse("", content_type="text/plain"), name="robots_file"),

    # https://acm.mst.edu/
    path('', views.index, name="index"),
    # https://acm.mst.edu/calendar/
    path('calendar/', views.calendar, name="calendar"),
    # https://acm.mst.edu/media/
    path('media/', views.media, name="media"),
    # https://acm.mst.edu/membership/
    path('membership/', views.Membership.as_view(), name="membership"),
    # https://acm.mst.edu/officers/
    path('officers/', views.officers, name="officers"),
    # https://acm.mst.edu/sigs/
    path('sigs/', views.sigs, name="sigs"),
    # https://acm.mst.edu/sponsors/
    path('sponsors/', views.Sponsors.as_view(), name="sponsors"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
