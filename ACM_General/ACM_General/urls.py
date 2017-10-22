# Django
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^social-auth/', include('thirdparty_auth.urls')),
    url(r'^web-api/', include('rest_api.urls')),
    url(r'^account/', include('accounts.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^', include('home.urls')),
]
