from django.conf.urls import url
from . import views


app_name = 'payments'
urlpatterns = [
    # acm.mst.edu/membership/
    url(r'membership/', views.MembershipPayment.as_view(), name='acm-memberships'),

    # acm.mst.edu/productHandler/<pk>/
    url(r'productHandler/(?P<pk>[0-9a-z-]+)/', views.ProductHandler.as_view(), name='product-handler'),
]
