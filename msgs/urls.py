from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/$', views.ThreadListView.as_view(), name='thread-listview'),

    url(r'^send/$', views.send_msg, name='send-msg'),

    url(r'^fetch/(?P<pk>\d+)/$', views.fetch_msg, name='fetch-msg'),
]
