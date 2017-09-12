from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create/$', views.InventoryCreateView.as_view(), name='inventory_create'),
    url(r'^(?P<pk>\d+)/edit/', views.InventoryUpdateView.as_view(), name='inventory_updateview'),
    url(r'^list/$', views.InventoryListView.as_view(), name='inventory_listview'),
    url(r'^(?P<pk>\d+)/', views.InventoryDetailView.as_view(), name='inventory_detailview'),
    url(r'^search/$', views.search, name='search'),

    url(r'^increase/quantity/(?P<pk>\d+)/$', views.increase_quantity, name='increase_quantity'),
    url(r'^decrease/quantity/(?P<pk>\d+)/$', views.decrease_quantity, name='decrease_quantity'),
]
