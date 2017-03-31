from django.conf.urls import url

from . import views, api_views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^inventory/$', views.inventory_list, name='inventory_list'),
    url(r'^inventory/create/$', views.inventory_create, name='inventory_create'),
    url(r'^inventory/edit/(?P<pk>\d+)/$', views.inventory_edit, name='inventory_edit'),

    url(r'^worksheet/$', views.worksheet_list, name='worksheet_list'),
    url(r'^worksheet/create/$', views.worksheet_create, name='worksheet_create'),
    url(r'^worksheet/edit/(?P<pk>\d+)/$', views.worksheet_edit, name='worksheet_edit'),

    # API

    url(r'^fetch/item/details/(?P<part_no>.*)/$', api_views.fetch_item_details, name='fetch_item_details'),
    url(r'^get/past/price/(?P<part_no>.*)/$', api_views.get_past_price, name='get_past_price'),

    url(r'^cost/price/toggle/(?P<pk>\d+)/$', api_views.cost_price_toggle, name='cost_price_toggle'),
    url(r'^sale/price/toggle/(?P<pk>\d+)/$', api_views.sale_price_toggle, name='sale_price_toggle'),
    url(r'^total/price/toggle/(?P<pk>\d+)/$', api_views.total_toggle, name='total_toggle'),
]
