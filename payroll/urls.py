from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^date/range/$', views.date_range, name='date_range'),
]
