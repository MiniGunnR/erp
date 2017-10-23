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

    url(r'^lc/create/$', views.LCCreateView.as_view(), name='lc_createview'),
    url(r'^lc/(?P<pk>\d+)/$', views.LCUpdateView.as_view(), name='lc_updateview'),
    url(r'^lc/list/$', views.LCListView.as_view(), name='lc_listview'),
    url(r'^lc/search/$', views.lc_search, name='lc_search'),

    url(r'^yarn/rcvd/create/$', views.YRCreateView.as_view(), name='yr_createview'),
    url(r'^yarn/rcvd/(?P<pk>\d+)/$', views.YRUpdateView.as_view(), name='yr_updateview'),
    url(r'^yarn/rcvd/list/$', views.YRListView.as_view(), name='yr_listview'),
    url(r'^yarn/rcvd/search/$', views.yr_search, name='yr_search'),

    url(r'^yarn/del/create/$', views.YDCreateView.as_view(), name='yd_createview'),
    url(r'^yarn/del/(?P<pk>\d+)/$', views.YDUpdateView.as_view(), name='yd_updateview'),
    url(r'^yarn/del/list/$', views.YDListView.as_view(), name='yd_listview'),
    url(r'^yarn/del/search/$', views.yd_search, name='yd_search'),

    url(r'^fabric/del/create/$', views.FDCreateView.as_view(), name='fd_createview'),
    url(r'^fabric/del/(?P<pk>\d+)/$', views.FDUpdateView.as_view(), name='fd_updateview'),
    url(r'^fabric/del/list/$', views.FDListView.as_view(), name='fd_listview'),
    url(r'^fabric/del/search/$', views.fd_search, name='fd_search'),
]
