from django.shortcuts import render
from django.views.generic import DetailView
from datetime import datetime

from .models import Requisition, Item, PurchaseOrder


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


def purchase_order(request, pk):
    requisition = Requisition.objects.get(id=pk)
    items = Item.objects.filter(requisition=requisition)

    year = datetime.now().year
    reference_no = "PO-DAL-{year}-{ref_id}".format(year=str(year), ref_id=str(requisition.id).zfill(4))

    po, created = PurchaseOrder.objects.get_or_create(requisition=requisition, defaults={ "reference_no": reference_no })
    context = {
        "object": requisition,
        "items": items,
        "po": po,
    }
    return render(request, "requisition/purchase_order.html", context)
