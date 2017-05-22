from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^employees/$', views.employee_list, name='employee_list'),

    url(r'^summary/(?P<month>\w+)/(?P<year>\d{4})/$', views.month_summary, name='month_summary'),
    url(r'^(?P<employee_id>\d+)/(?P<year>\d{4})/', views.employee_summary, name='employee_summary'),
    url(r'^summary/(?P<year>\d{4})/$', views.year_summary, name='year_summary'),
    url(r'^action/$', views.action, name='action'),

    url(r'^populate/$', views.populate, name='populate'),
    url(r'^select/by/date/(?P<date>\d+)/$', views.select_by_date, name='select_by_date'),
]
