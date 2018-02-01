"""
Contains the urls for the `/web_api/` route.
"""
# third-party
from rest_framework.urlpatterns import format_suffix_patterns

# Django
from django.urls import path

# local Django
from . import views


app_name = 'rest_api'
urlpatterns = [
    # acm.mst.edu/web-api/accounts/
    path('accounts/', views.UserList.as_view(), name='user-list'),

    # acm.mst.edu/web-api/accounts/<pk>/
    path(
        'accounts/<uuid:pk>/',
        views.UserDetail.as_view(),
        name='user-detail'
    ),

    # acm.mst.edu/web-api/events/
    path('events/', views.EventList.as_view(), name='event-list'),

    # acm.mst.edu/web-api/events/<pk>/
    path(
        'events/<uuid:pk>/',
        views.EventDetail.as_view(),
        name='event-detail'
    ),

    # acm.mst.edu/web-api/sigs/
    path('sigs/', views.SIGList.as_view(), name='sig-list'),

    # acm.mst.edu/web-api/sigs/<pk>/
    path(
        'sigs/<str:pk>/',
        views.SIGDetail.as_view(),
        name='sig-detail'
    ),

    # acm.mst.edu/web-api/transactions/
    path(
        'transactions/',
        views.TransactionList.as_view(),
        name='transaction-list'
    ),

    # acm.mst.edu/web-api/transactions/<pk>/
    path(
        'transactions/<uuid:pk>/',
        views.TransactionDetail.as_view(),
        name='transaction-detail'
    ),

    # acm.mst.edu/web-api/product/
    path('products/', views.ProductList.as_view(), name='product-list'),

    # acm.mst.edu/web-api/product/<pk>/
    path(
        'products/<str:pk>/',
        views.ProductDetail.as_view(),
        name='product-detail'
    ),

    # acm.mst.edu/web-api/category/
    path('categories/', views.CategoryList.as_view(), name='category-list'),

    # acm.mst.edu/web-api/category/<pk>/
    path(
        'categories/<uuid:pk>/',
        views.CategoryDetail.as_view(),
        name='category-detail'
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
