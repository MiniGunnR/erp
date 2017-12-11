from django.conf.urls import url

from . import views

app_name='ticket'
urlpatterns = [
    url(r'^$', views.ticket_list, name='ticket_list'),
    url(r'^applied/$', views.AppliedListView.as_view(), name='applied_listview'),
    url(r'^received/$', views.ReceivedListView.as_view(), name='received_listview'),
    url(r'^(?P<pk>\d+)/$', views.TicketDetailView.as_view(), name='ticket_detailview'),
    url(r'^create/$', views.TicketCreateView.as_view(), name='ticket_createview'),

    url(r'^(?P<pk>\d+)/mark/as/solved/$', views.mark_as_solved, name='mark_as_solved'),
    url(r'^(?P<pk>\d+)/deny/ticket/solution/$', views.deny_ticket_solution, name='deny_ticket_solution'),
    url(r'^(?P<pk>\d+)/accept/ticket/solution/$', views.accept_ticket_solution, name='accept_ticket_solution'),
]
