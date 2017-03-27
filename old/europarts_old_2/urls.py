from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^product/request/list/create/$', views.create_product_request_list, name='product-request-list-create'),
    url(r'^product/request/list/$', views.ProductRequestListView.as_view(), name='product-request-listview'),
    url(r'^product/request/detail/(?P<pk>\d+)/$', views.ProductRequestDetailView.as_view(), name='product-request-detail'),

    url(r'^add/cost/price/(?P<pk>\d+)/$', views.add_cost_price, name='add-cost-price'),
    url(r'^add/selling/price/(?P<pk>\d+)/$', views.add_selling_price, name='add-selling-price'),

    url(r'^create/quotation/$', views.create_quotation, name='create-quotation'),
    url(r'^add/item/to/quotation/(?P<pk>\d+)/$', views.add_item_to_quotation, name='add-item-to-quotation'),
    url(r'^remove/item/from/quotation/(?P<pk>\d+)/$', views.remove_item_from_quotation, name='remove-item-from-quotation'),
    url(r'^clear/quotation/', views.clear_quotation, name='clear-quotation'),
    url(r'^generate/quotation/$', views.generate_quotation, name='generate-quotation'),
    url(r'^list/quotations/$', views.QuotationListView.as_view(), name='quotation-listview'),
    url(r'^quotation/details/(?P<pk>\d+)/$', views.quotation_details, name='quotation-details'),
    url(r'^quotation/details/(?P<pk>\d+)/access/code/$', views.quotation_access_code, name='quotation-access-code'),


    # API

    url(r'^filter/auto/type/with/brand/(?P<pk>\d+)/$', views.filter_auto_type_with_brand, name='filter-auto-type-with-brand'),
    url(r'^fetch/from/part/no/(?P<part_no>.+)/brand/(?P<brand_pk>\d+)/$', views.fetch_auto_part, name='fetch-auto-part'),
    url(r'^fetch/product/from/auto/part/(?P<pk>\d+)/$', views.fetch_product, name='fetch-product'),
    url(r'^disable/work/order/print/(?P<pk>\d+)/$', views.disable_work_order_print, name='disable-work-order-print'),
]
