# from django.shortcuts import render, reverse
# from django.views import generic
# from django.http import HttpResponseRedirect
# from django.db.models import Q
# from django.db import transaction
#
#
# from .models import Inventory, LetterOfCredit, LCItem, YarnReceived, YarnIssue, FabricDelivery
# from .forms import QuantityForm, LC_Formset, LcSearchForm, YrSearchForm, YiSearchForm, FdSearchForm, FdForm
#
#
# class LCCreateView(generic.CreateView):
#     model = LetterOfCredit
#     fields = ['date', 'number', 'spinning_mill']
#     template_name = "inv/lc_form.html"
#
#     def get_success_url(self):
#         return reverse('inv:lc_updateview', args=[self.object.pk])
#
#     def get_context_data(self, **kwargs):
#         context = super(LCCreateView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             context['lc_items'] = LC_Formset(self.request.POST)
#         else:
#             context['lc_items'] = LC_Formset()
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         lc_items = context['lc_items']
#         with transaction.atomic():
#             self.object = form.save()
#             if lc_items.is_valid():
#                 lc_items.instance = self.object
#                 lc_items.save()
#         return super(LCCreateView, self).form_valid(form)
#
#
# class LCUpdateView(generic.UpdateView):
#     model = LetterOfCredit
#     fields = ['date', 'number', 'spinning_mill']
#     template_name = "inv/lc_form.html"
#
#     def get_success_url(self):
#         return reverse('inv:lc_updateview', args=[self.object.pk])
#
#     def get_context_data(self, **kwargs):
#         context = super(LCUpdateView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             context['lc_items'] = LC_Formset(self.request.POST, instance=self.object)
#         else:
#             context['lc_items'] = LC_Formset(instance=self.object)
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         lc_items = context['lc_items']
#         with transaction.atomic():
#             self.object = form.save()
#             if lc_items.is_valid():
#                 lc_items.instance = self.object
#                 lc_items.save()
#         return super(LCUpdateView, self).form_valid(form)
#
#
# class LCListView(generic.ListView):
#     model = LetterOfCredit
#     template_name = "inv/lc_listview.html"
#
#     def get_queryset(self):
#         if self.request.GET.get('q', ''):
#             return LetterOfCredit.objects.filter(number__icontains=self.request.GET['q'])
#         return LetterOfCredit.objects.all()
#
#
# def lc_search(request):
#     form = LcSearchForm(request.POST or None)
#     c = {
#         "form": form,
#     }
#     return render(request, "inv/lc_search.html", c)
#
#
# class YRCreateView(generic.CreateView):
#     model = YarnReceived
#     template_name = "inv/yr_form.html"
#     fields = ['date', 'barcode', 'lc_item', 'challan_no', 'quantity']
#
#     def get_success_url(self):
#         if self.object.pk:
#             return reverse('inv:yr_updateview', args=[self.object.pk])
#         return
#
#
# class YRUpdateView(generic.UpdateView):
#     model = YarnReceived
#     template_name = "inv/yr_form.html"
#     fields = ['date', 'barcode', 'lc_item', 'challan_no', 'quantity']
#
#     def get_success_url(self):
#         return reverse('inv:yr_updateview', args=[self.object.pk])
#
#
# class YRListView(generic.ListView):
#     model = YarnReceived
#     template_name = "inv/yr_listview.html"
#
#     def get_queryset(self):
#         if self.request.GET.get('q', ''):
#             return YarnReceived.objects.filter(barcode__icontains=self.request.GET['q'])
#         return YarnReceived.objects.all()
#
#
# def yr_search(request):
#     form = YrSearchForm(request.POST or None)
#     c = {
#         "form": form,
#     }
#     return render(request, "inv/yr_search.html", c)
#
#
# class YICreateView(generic.CreateView):
#     model = YarnIssue
#     template_name = "inv/yi_form.html"
#     fields = ['yr', 'date', 'barcode', 'challan_no', 'colour', 'style_no', 'quantity', 'knitting_factory_name', 'machine_brand', 'machine_dia', 'grey_finished_dia', 'machine_gauge', 'finished_garments_quality']
#
#
# class YIUpdateView(generic.UpdateView):
#     model = YarnIssue
#     template_name = "inv/yi_form.html"
#     fields = ['yr', 'date', 'barcode', 'challan_no', 'colour', 'style_no', 'quantity', 'knitting_factory_name', 'machine_brand', 'machine_dia', 'grey_finished_dia', 'machine_gauge', 'finished_garments_quality']
#
#
# class YIListView(generic.ListView):
#     model = YarnIssue
#     template_name = "inv/yi_listview.html"
#
#     def get_queryset(self):
#         if self.request.GET.get('q', ''):
#             return YarnIssue.objects.filter(barcode__icontains=self.request.GET['q'])
#         return YarnIssue.objects.all()
#
#
# def yi_search(request):
#     form = YiSearchForm(request.POST or None)
#     c = {
#         "form": form,
#     }
#     return render(request, "inv/yi_search.html", c)
#
#
# class FDCreateView(generic.CreateView):
#     form_class = FdForm
#     model = FabricDelivery
#     template_name = "inv/fd_form.html"
#
#
# class FDUpdateView(generic.UpdateView):
#     form_class = FdForm
#     model = FabricDelivery
#     template_name = "inv/fd_form.html"
#
#
# class FDListView(generic.ListView):
#     model = FabricDelivery
#     template_name = "inv/fd_listview.html"
#
#     def get_queryset(self):
#         if self.request.GET.get('q', ''):
#             return FabricDelivery.objects.filter(barcode__icontains=self.request.GET['q'])
#         return FabricDelivery.objects.all()
#
#
# def fd_search(request):
#     form = FdSearchForm(request.POST or None)
#     c = {
#         "form": form,
#     }
#     return render(request, "inv/fd_search.html", c)
#
#
# class InventoryCreateView(generic.CreateView):
#     model = Inventory
#     template_name = "inv/inventory_createview.html"
#     fields = ['uid', 'name', 'quantity', 'lc', 'spinning_mills', 'composition']
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super(InventoryCreateView, self).form_valid(form)
#
#
# class InventoryListView(generic.ListView):
#     model = Inventory
#     template_name = "inv/inventory_listview.html"
#
#
# class InventoryDetailView(generic.DetailView):
#     model = Inventory
#     template_name = "inv/inventory_detailview.html"
#
#
# class InventoryUpdateView(generic.UpdateView):
#     model = Inventory
#     template_name = "inv/inventory_updateview.html"
#     fields = ['uid', 'name', 'quantity', 'lc', 'spinning_mills', 'composition']
#
#     def form_valid(self, form):
#         form.instance.modified_by = self.request.user
#         return super(InventoryUpdateView, self).form_valid(form)
#
#
# def search(request):
#     query = request.GET.get('q', '')
#
#     if query == '':
#         objs = Inventory.objects.none()
#     else:
#         objs = Inventory.objects.filter(
#             Q(uid=query) |
#             Q(lc=query) |
#             Q(name__icontains=query)
#         )
#
#     context = {
#         "objs": objs,
#     }
#
#     return render(request, "inv/search.html", context)
#
#
#
# def increase_quantity(request, pk):
#     item = Inventory.objects.get(id=pk)
#     uid = item.uid
#     if request.method == "POST":
#         form = QuantityForm(request.POST)
#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']
#             item.quantity += quantity
#             item.save()
#             return HttpResponseRedirect(reverse('inv:inventory_detailview', args=[item.pk]))
#     else:
#         form = QuantityForm()
#     context = {
#         "form": form,
#         "uid": uid,
#         "pk": pk,
#     }
#     return render(request, "inv/increase_quantity.html", context)
#
#
# def decrease_quantity(request, pk):
#     item = Inventory.objects.get(id=pk)
#     uid = item.uid
#     if request.method == "POST":
#         form = QuantityForm(request.POST)
#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']
#             item.quantity -= quantity
#             item.save()
#             return HttpResponseRedirect(reverse('inv:inventory_detailview', args=[item.pk]))
#     else:
#         form = QuantityForm()
#     context = {
#         "form": form,
#         "uid": uid,
#         "pk": pk,
#     }
#     return render(request, "inv/decrease_quantity.html", context)
#
