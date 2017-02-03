from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^create/user/$', views.create_user, name='create-user'),
]
