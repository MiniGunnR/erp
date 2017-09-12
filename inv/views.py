from django.shortcuts import render, reverse
from django.views import generic
from django.http import HttpResponseRedirect

from .models import Inventory
from .forms import QuantityForm


class InventoryCreateView(generic.CreateView):
    model = Inventory
    template_name = "inv/inventory_createview.html"
    fields = ['uid', 'name', 'quantity', 'lc', 'spinning_mills', 'composition']


class InventoryListView(generic.ListView):
    model = Inventory
    template_name = "inv/inventory_listview.html"


class InventoryDetailView(generic.DetailView):
    model = Inventory
    template_name = "inv/inventory_detailview.html"


class InventoryUpdateView(generic.UpdateView):
    model = Inventory
    template_name = "inv/inventory_updateview.html"
    fields = ['uid', 'name', 'quantity', 'lc', 'spinning_mills', 'composition']


def search(request):
    query = request.GET.get('q', '')

    if query == '':
        objs = Inventory.objects.none()
    else:
        objs = Inventory.objects.filter(uid__icontains=query)

    context = {
        "objs": objs,
    }

    return render(request, "inv/search.html", context)



def increase_quantity(request, pk):
    item = Inventory.objects.get(id=pk)
    uid = item.uid
    if request.method == "POST":
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            item.quantity += quantity
            item.save()
            return HttpResponseRedirect(reverse('inv:inventory_detailview', args=[item.pk]))
    else:
        form = QuantityForm()
    context = {
        "form": form,
        "uid": uid,
        "pk": pk,
    }
    return render(request, "inv/increase_quantity.html", context)


def decrease_quantity(request, pk):
    item = Inventory.objects.get(id=pk)
    uid = item.uid
    if request.method == "POST":
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            item.quantity -= quantity
            item.save()
            return HttpResponseRedirect(reverse('inv:inventory_detailview', args=[item.pk]))
    else:
        form = QuantityForm()
    context = {
        "form": form,
        "uid": uid,
        "pk": pk,
    }
    return render(request, "inv/decrease_quantity.html", context)

