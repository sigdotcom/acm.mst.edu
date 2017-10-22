# Django
from django.conf.urls import url

# local Django
from . import views


app_name = 'products'
urlpatterns = [
    # acm.mst.edu/products/membership/semester/
    url(
        r'membership/semester/',
        views.MembershipPayment.as_view(),
        name='membership-semester'
    ),
    # acm.mst.edu/products/membership/year/
    url(
        r'membership/year/',
        views.MembershipPayment.as_view(),
        name='membership-year'
    ),
    # acm.mst.edu/products/membership/year/
    url(
        r'sponsorship/',
        views.MembershipPayment.as_view(),
        name='sponsorship'
    ),
]
