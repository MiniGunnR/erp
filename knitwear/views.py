from django.shortcuts import render, reverse
from django.views import generic

from .models import Item, OrderCollection


class ItemCreateView(generic.CreateView):
    model = Item
    fields = ['name']
    template_name = "knitwear/item_create.html"

    def get_success_url(self):
        return reverse('knitwear:order_collection_createview')


class OrderCollectionCreateView(generic.CreateView):
    model = OrderCollection
    fields = ['item', 'order_no', 'style', 'quantity', 'unit_price', 'total']
    template_name = "knitwear/order_collection.html"

    def get_success_url(self):
        return reverse('knitwear:order_collection_listview')


class OrderCollectionListView(generic.ListView):
    model = OrderCollection
    fields = ['item', 'order_no', 'style', 'quantity', 'unit_price', 'total']
    template_name = "knitwear/order_collection_list.html"
