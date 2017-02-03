from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^create/product/request/list/$', views.create_product_request_list, name='create-product-request-list'),
]
