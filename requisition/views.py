from django.shortcuts import render
from django.views.generic import DetailView

from .models import Requisition, Item


def home(request):
    return render(request, "requisition/home.html")


def create_requisition(request):
    return render(request, "requisition/create-requisition.html")


class RequisitionDetailView(DetailView):
    model = Requisition
    template_name = "requisition/requisition_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(RequisitionDetailView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(requisition=self.object)
        return context


class PurchaseOrderDetailView(DetailView):
    model = Requisition
    template_name = "requisition/purchase_order.html"

    def get_context_data(self, **kwargs):
        context = super(PurchaseOrderDetailView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(requisition=self.object)
        return context