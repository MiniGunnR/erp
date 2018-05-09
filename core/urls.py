from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^initial/$', views.initial, name='initial'),

    url(r'^create/user/$', views.create_user, name='create-user'),
    url(r'^create/bulk/users/$', views.create_bulk_user, name='create-bulk-user'),

    url(r'^login/$', login, name="my_login", kwargs={'redirect_authenticated_user': True}),
    url(r'^logout/$', logout, name="my_logout"),

    url(r'^db/backup/$', views.db_backup, name='db_backup'),

    url(r'^mailbox/$', views.Mailbox.as_view(), name='mailbox'),
]
