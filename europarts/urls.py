from django.conf.urls import url

from . import views, api_views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^worksheet/$', views.worksheet_list, name='worksheet_list'),
    url(r'^worksheet/create/$', views.worksheet_create, name='worksheet_create'),
    url(r'^worksheet/edit/(?P<pk>\d+)/$', views.worksheet_edit, name='worksheet_edit'),

    url(r'^cost/price/toggle/(?P<pk>\d+)/$', api_views.cost_price_toggle, name='cost_price_toggle'),
    url(r'^sale/price/toggle/(?P<pk>\d+)/$', api_views.sale_price_toggle, name='sale_price_toggle'),
    url(r'^total/price/toggle/(?P<pk>\d+)/$', api_views.total_toggle, name='total_toggle'),
]
