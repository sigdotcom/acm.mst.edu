# Django
from django.conf.urls import url

# local Django
from . import views


app_name = 'payments'
urlpatterns = [
    # acm.mst.edu/productHandler/<pk>/
    url(
        r'productHandler/(?P<tag>[0-9a-z-]+)/',
        views.ProductHandler.as_view(),
        name='product-handler'
    ),
]
