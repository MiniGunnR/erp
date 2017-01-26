from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^select/date/$', views.select_date, name='select-date'),
]
