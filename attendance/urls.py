from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.attendance, name='attendance'),

    url(r'^select/by/date/$', views.select_by_date, name='select-by-date'),
    url(r'^select/by/month/$', views.select_by_month, name='select-by-month'),
]

