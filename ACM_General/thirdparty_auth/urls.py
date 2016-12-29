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

from thirdparty_auth.views import index, googleCallback, googleCallback2

app_name = 'thirdparty_auth'
urlpatterns = [
    url(r'^login/(?P<auth_backend>[a-z])/$', index, name='login'),
    url(r'^register/(?P<auth_backend>[a-z])/$', index, name='login'),
    url(r'^google-callback/$', googleCallback, name='google_oauth2_callback'),
    url(r'^google-callback2/$', googleCallback2, name='google_oauth22_callback'),
]
