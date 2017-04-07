"""ACM_General URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^social-auth/', include('thirdparty_auth.urls')),
    url(r'^web-api/', include('rest_api.urls')),
    url(r'^account/', include('accounts.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^payments/', include('payments.urls')),
    url(r'^', include('home.urls')),
    url(r'^tz_detect/', include('tz_detect.urls')),
]
