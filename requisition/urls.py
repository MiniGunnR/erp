from django.conf.urls import url
from wkhtmltopdf.views import PDFTemplateView

from . import views

app_name='requisition'
urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^create/$', views.create_requisition, name='create-requisition'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit_requisition, name='edit-requisition'),

    url(r'^(?P<pk>\d+)/$', views.RequisitionDetailView.as_view(), name='requisition-detail-view'),
    url(r'^(?P<pk>\d+)/purchase/order/$', views.purchase_order, name='purchase-order'),

    url(r'^(?P<pk>\d+)/pdf/$', views.RequisitionView.as_view(), name='requisition-pdf-view'),
    # url(r'^(?P<pk>\d+)/pdf/$', PDFTemplateView.as_view(template_name='requisition/requisition_template.html', filename='requisition.pdf'), name='requisition_view'),
    url(r'^quotation/request/email/(?P<pk>\d+)/$', views.QuotationRequestEmail.as_view(), name='quotationrequest_email'),
]
