from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "home"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'sponsors/', views.sponsors, name="sponsors"),
    url(r'calendar/', views.calendar, name="calendar"),
    url(r'media/', views.media, name="media"),
    url(r'officers/', views.officers, name="officers"),
    url(r'membership/', views.membership, name="membership"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
