from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^initial/$', views.initial, name='initial'),

    url(r'^create/user/$', views.create_user, name='create-user'),

    url(r'^login/$', login, name="my_login"),
    url(r'^logout/$', logout, name="my_logout"),
]
