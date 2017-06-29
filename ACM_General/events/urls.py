"""
ACM_General URL Configuration
-----------------------------

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/1.10/topics/http/urls/

Examples:

Function views
--------------
#. Add an import:  from my_app import views
#. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')

Class-based views
-----------------

#. Add an import:  from other_app.views import Home
#. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')

Including another URLconf
-------------------------

#. Import the include() function: from django.conf.urls import url, include
#. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from events import views

app_name = 'events'
urlpatterns = [
    # acm.mst.edu/events/
    url('^$', views.list_events, name='events-list'),

    # acm.mst.edu/events/create/
    url('create/$', views.create_event, name='create-event'),
]
