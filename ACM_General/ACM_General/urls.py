# Django
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social-auth/', include('thirdparty_auth.urls')),
    path('web-api/', include('rest_api.urls')),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('products/', include('products.urls')),
    path('', include('home.urls')),
    path('tools/', include('tools.urls')),
]
