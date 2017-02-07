from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^product/request/list/$', views.ProductRequestListView.as_view(), name='product-request-listview'),
    url(r'^product/request/list/create/$', views.create_product_request_list, name='product-request-list-create'),
    url(r'^product/request/list/(?P<pk>\d+)/edit/$', views.edit_product_request_list, name='edit-product-request-list'),

    url(r'^get/part/(?P<part_no>\d+)/info/$', views.get_part_info, name='get-part-info'),
]
