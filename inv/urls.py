from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^lc/create/$', views.LCCreateView.as_view(), name='lc_createview'),
    url(r'^lc/update/(?P<pk>\d+)/$', views.LCUpdateView.as_view(), name='lc_updateview'),
    url(r'^lc/list/$', views.LCListView.as_view(), name='lc_listview'),
    url(r'^lc/(?P<pk>\d+)/$', views.LCDetailView.as_view(), name='lc_detailview'),
    url(r'^lc/search/$', views.LCSearchView.as_view(), name='lc_searchview'),
    url(r'^lc/search/result/$', views.LCSearchResultListView.as_view(), name='lc_search_result_listview'),

    url(r'^yarn/rcv/create/(?P<lc_item_pk>\d+)/$', views.YarnRcvCreateView.as_view(), name='yarn_rcv_createview'),
    url(r'^yarn/rcv/list/$', views.YarnRcvListView.as_view(), name='yarn_rcv_listview'),
    url(r'^yarn/rcv/search/$', views.YarnRcvSearchView.as_view(), name='yarn_rcv_searchview'),
    url(r'^yarn/rcv/search/result/$', views.YarnRcvSearchResultListView.as_view(), name='yarn_rcv_search_result_listview'),

    url(r'^yarn/issue/create/(?P<lc_item_pk>\d+)$', views.YarnIssueCreateView.as_view(), name='yarn_issue_createview'),
    url(r'^yarn/issue/list/$', views.YarnIssueListView.as_view(), name='yarn_issue_listview'),
    url(r'^yarn/issue/search/$', views.YarnIssueSearchView.as_view(), name='yarn_issue_searchview'),
    url(r'^yarn/issue/search/result/$', views.YarnIssueSearchResultView.as_view(), name='yarn_issue_search_result_listview'),

    url(r'^fabric/delivery/create/$', views.FabricDeliveryCreateView.as_view(), name='fabric_delivery_createview'),
    url(r'^fabric/delivery/list/$', views.FabricDeliveryListView.as_view(), name='fabric_delivery_listview'),
    url(r'^fabric/delivery/search/$', views.FabricDeliverySearchView.as_view(), name='fabric_delivery_search'),
    url(r'^fabric/delivery/search/result/$', views.FabricDeliverySearchResultView.as_view(), name='fabric_delivery_search_result_listview')
]
