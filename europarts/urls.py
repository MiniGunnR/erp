from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^worksheet/$', views.worksheet_list, name='worksheet_list'),
    url(r'^worksheet/create/$', views.worksheet_create, name='worksheet_create'),
]
