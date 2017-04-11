from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^check/balance/$', views.check_employee_balance, name='check-employee-balance'),
    url(r'^list/$', views.billing_list, name='billing_list'),
]
