from django.conf.urls import url

from . import views, api_views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^inventory/$', views.inventory_list, name='inventory_list'),
    url(r'^inventory/create/$', views.inventory_create, name='inventory_create'),
    url(r'^inventory/edit/(?P<pk>\d+)/$', views.inventory_edit, name='inventory_edit'),
    url(r'^inventory/add/quantity/(?P<pk>\d+)/', views.inventory_quantity_add, name='inventory_quantity_add'),

    url(r'^worksheet/$', views.worksheet_list, name='worksheet_list'),
    url(r'^worksheet/create/$', views.worksheet_create, name='worksheet_create'),
    url(r'^worksheet/edit/(?P<pk>\d+)/$', views.worksheet_edit, name='worksheet_edit'),

    url(r'^bill/$', views.bill_list, name='bill_list'),
    url(r'^bill/create/$', views.bill_create, name='bill_create'),
    url(r'^bill/edit/(?P<pk>\d+)/$', views.bill_edit, name='bill_edit'),

    url(r'^quotation/$', views.quotation_list, name='quotation_list'),
    url(r'^quotation/create/from/worksheet/(?P<ws_id>\d+)/$', views.quotation_create, name='quotation_create'),
    url(r'^quotation/details/(?P<pk>\d+)/$', views.quotation_details, name='quotation_details'),
    url(r'^quotation/email/(?P<pk>\d+)$', views.QuotationEmail.as_view(), name='quotation_email'),

    url(r'^invoice/$', views.invoice_list, name='invoice_list'),
    url(r'^invoice/create/from/quotation/(?P<qt_id>\d+)/$', views.invoice_create, name='invoice_create'),
    url(r'^invoice/details/(?P<pk>\d+)/$', views.invoice_details, name='invoice_details'),
    url(r'^invoice/email/(?P<pk>\d+)$', views.InvoiceEmail.as_view(), name='invoice_email'),

    url(r'^challan/$', views.challan_list, name='challan_list'),
    url(r'^challan/details/(?P<pk>\d+)/$', views.challan_details, name='challan_details'),

    # API

    url(r'^fetch/item/details/(?P<part_no>.*)/$', api_views.fetch_item_details, name='fetch_item_details'),
    url(r'^get/past/price/(?P<part_no>.*)/$', api_views.get_past_price, name='get_past_price'),

    url(r'^cost/price/toggle/(?P<pk>\d+)/$', api_views.cost_price_toggle, name='cost_price_toggle'),
    url(r'^sale/price/toggle/(?P<pk>\d+)/$', api_views.sale_price_toggle, name='sale_price_toggle'),
    url(r'^total/price/toggle/(?P<pk>\d+)/$', api_views.total_toggle, name='total_toggle'),
]

