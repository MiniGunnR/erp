from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),

    url(r'^create/$', views.create_requisition, name='create-requisition'),

    url(r'^(?P<pk>\d+)/$', views.RequisitionDetailView.as_view(), name='requisition-detail-view'),
    url(r'^(?P<pk>\d+)/purchase/order/$', views.PurchaseOrderDetailView.as_view(), name='purchase-order-detail-view'),
]
