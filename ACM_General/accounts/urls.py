from django.conf.urls import url
from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'logout/', views.user_logout, name='user-logout'),
    url(r'login/', views.user_login, name='user-login'),
]
