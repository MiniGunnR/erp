from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^item/$', views.ItemCreateView.as_view(), name='item_createview'),
    url(r'^order/collection/$', views.OrderCollectionCreateView.as_view(), name='order_collection_createview'),
    url(r'^order/collection/list/$', views.OrderCollectionListView.as_view(), name='order_collection_listview'),
]
