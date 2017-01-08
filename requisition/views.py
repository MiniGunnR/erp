from django.shortcuts import render
from django.views.generic import DetailView

from .models import Requisition, Item

class RequisitionDetailView(DetailView):
    model = Requisition
    template_name = "requisition/requisition_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(RequisitionDetailView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(requisition=self.object)
        return context
