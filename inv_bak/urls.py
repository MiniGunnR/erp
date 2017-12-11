from django.conf.urls import url

from . import views


urlpatterns = [
  url('^lc/create/$', views.LCCreateView.as_view(), name='lc_createview'),
  url('^lc/update/(?P<pk>\d+)/$', views.LCUpdateView.as_view(), name='lc_updateview'),
  url('^lc/list/$', views.LCListView.as_view(), name='lc_listview'),
  url('^lc/(?P<pk>\d+)/$', views.LCDetailView.as_view(), name='lc_detailview'),
  url('^lc/search/$', views.LCSearchView.as_view(), name='lc_searchview'),
  url('^lc/search/result/$', views.LCSearchResultListView.as_view(), name='lc_search_result_listview'),

  url('yarn/rcv/create/(?P<lc_item_pk>\d+)/$', views.YarnRcvCreateView.as_view(), name='yarn_rcv_createview'),
]
