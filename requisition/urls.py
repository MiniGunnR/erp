from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^create/$', views.create_requisition, name='create-requisition'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit_requisition, name='edit-requisition'),

    url(r'^(?P<pk>\d+)/$', views.RequisitionDetailView.as_view(), name='requisition-detail-view'),
    url(r'^(?P<pk>\d+)/purchase/order/$', views.purchase_order, name='purchase-order'),
]

