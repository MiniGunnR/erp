from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^employees/$', views.employees, name='employees'),
    url(r'^(?P<month>\d{1,2})/(?P<year>\d{4})/$', views.month_summary, name='month_summary'),
    url(r'^action/$', views.action, name='action'),

    url(r'^(?P<employee_id>\d{10})/(?P<year>\d{4})/$', views.employee_summary, name='employee_summary'),


    url(r'^off/day/entry/$', views.off_day_entry, name='off_day_entry'),


    url(r'^pull/$', views.pull, name='pull'),
    url(r'^populate/$', views.populate, name='populate'),
    url(r'^select/by/date/(?P<date>\d+)/$', views.select_by_date, name='select_by_date'),
]

