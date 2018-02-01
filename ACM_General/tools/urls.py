# Django
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

# local Django
from . import views

app_name = "tools"
urlpatterns = [
    # https://acm.mst.edu/
    url(r'^membership/$', views.membership, name="membership"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
