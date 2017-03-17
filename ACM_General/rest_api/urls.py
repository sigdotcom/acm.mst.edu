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
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'rest_api'
urlpatterns = [
    url('accounts/$', views.UserList.as_view(), name='user-list'),
    url('accounts/(?P<pk>[0-9a-z-]+)/$',
        views.UserDetail.as_view(),
        name='user-detail'
        ),
    url('events/$', views.EventList.as_view(), name='event-list'),
    url('events/(?P<pk>[0-9a-z-]+)/$',
        views.EventDetail.as_view(),
        name='event-detail'
        ),
    url('sigs/$', views.SIGList.as_view(), name='sigs-list'),
    url('sigs/(?P<pk>[0-9a-z-]+)/$',
        views.SIGDetail.as_view(),
        name='sigs-detail'
        ),
    url('transactions/$', views.TransactionList.as_view(), name='transaction-list'),
    url('transactions/(?P<pk>[0-9a-z-]+)/$',
        views.TransactionDetail.as_view(),
        name='transaction-detail'
        ),
    url('product/$', views.ProductList.as_view(), name='product-list'),
    url('product/(?P<pk>[0-9a-z-]+)/$',
        views.ProductDetail.as_view(),
        name='product-detail'
        ),
    url('category/$', views.CategoryList.as_view(), name='category-list'),
    url('category/(?P<pk>[0-9a-z-]+)/$',
        views.CategoryDetail.as_view(),
        name='category-detail'
        ),

]

urlpatterns = format_suffix_patterns(urlpatterns)
