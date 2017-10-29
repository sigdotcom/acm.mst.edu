"""
Contains the urls for the `/web_api/` route.
"""
# third-party
from rest_framework.urlpatterns import format_suffix_patterns

# Django
from django.conf.urls import url

# local Django
from . import views


app_name = 'rest_api'
urlpatterns = [
    # acm.mst.edu/web-api/accounts/
    url('accounts/$', views.UserList.as_view(), name='user-list'),

    # acm.mst.edu/web-api/accounts/<pk>/
    url(
        'accounts/(?P<pk>[0-9a-z_-]+)/$',
        views.UserDetail.as_view(),
        name='user-detail'
    ),

    # acm.mst.edu/web-api/events/
    url('events/$', views.EventList.as_view(), name='event-list'),

    # acm.mst.edu/web-api/events/<pk>/
    url(
        'events/(?P<pk>[0-9a-z_-]+)/$',
        views.EventDetail.as_view(),
        name='event-detail'
    ),

    # acm.mst.edu/web-api/sigs/
    url('sigs/$', views.SIGList.as_view(), name='sigs-list'),

    # acm.mst.edu/web-api/sigs/<pk>/
    url(
        'sigs/(?P<pk>[0-9a-z_-]+)/$',
        views.SIGDetail.as_view(),
        name='sigs-detail'
    ),

    # acm.mst.edu/web-api/transactions/
    url(
        'transactions/$',
        views.TransactionList.as_view(),
        name='transaction-list'
    ),

    # acm.mst.edu/web-api/transactions/<pk>/
    url(
        'transactions/(?P<pk>[0-9a-z_-]+)/$',
        views.TransactionDetail.as_view(),
        name='transaction-detail'
    ),

    # acm.mst.edu/web-api/product/
    url('product/$', views.ProductList.as_view(), name='product-list'),

    # acm.mst.edu/web-api/product/<pk>/
    url(
        'product/(?P<pk>[0-9a-z_-]+)/$',
        views.ProductDetail.as_view(),
        name='product-detail'
    ),

    # acm.mst.edu/web-api/category/
    url('category/$', views.CategoryList.as_view(), name='category-list'),

    # acm.mst.edu/web-api/category/<pk>/
    url(
        'category/(?P<pk>[0-9a-z_-]+)/$',
        views.CategoryDetail.as_view(),
        name='category-detail'
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
