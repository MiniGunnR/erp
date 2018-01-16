from django.shortcuts import render, reverse
from django.views import generic
from django.db import transaction

from .models import LC, LCItem, YarnRcv, YarnIssue, FabricDelivery

from .forms import LC_Formset, LCSearchForm, YarnRcvSearchForm, YarnIssueSearchForm, FabricDeliverySearchForm


class LCCreateView(generic.CreateView):
    model = LC
    fields = ['date', 'number', 'spinning_mill']
    template_name = 'inv/lc_form.html'

    def get_success_url(self):
        return reverse('inv:lc_updateview', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super(LCCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['lc_items'] = LC_Formset(self.request.POST)
        else:
            context['lc_items'] = LC_Formset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        lc_items = context['lc_items']
        with transaction.atomic():
            self.object = form.save()
            if lc_items.is_valid():
                lc_items.instance = self.object
                lc_items.save()
        return super(LCCreateView, self).form_valid(form)


class LCUpdateView(generic.UpdateView):
    model = LC
    fields = ['date', 'number', 'spinning_mill']
    template_name = 'inv/lc_form.html'

    def get_success_url(self):
        return reverse('inv:lc_updateview', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super(LCUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['lc_items'] = LC_Formset(self.request.POST, instance=self.object)
        else:
            context['lc_items'] = LC_Formset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        lc_items = context['lc_items']
        with transaction.atomic():
            self.object = form.save()
        if lc_items.is_valid():
            lc_items.instance = self.object
            lc_items.save()
        return super(LCUpdateView, self).form_valid(form)


class LCListView(generic.ListView):
    model = LC
    template_name = 'inv/lc_list.html'


class LCDetailView(generic.DetailView):
    model = LC
    template_name = 'inv/lc_detail.html'


class LCSearchView(generic.FormView):
    template_name = 'inv/lc_search.html'
    form_class = LCSearchForm


class LCSearchResultListView(generic.ListView):
    model = LC
    template_name = 'inv/lc_list.html'

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return LC.objects.filter(number__icontains=query)


class YarnRcvCreateView(generic.CreateView):
    model = YarnRcv
    fields = ['date', 'challan_no', 'lot', 'quantity_rcv']
    template_name = 'inv/yarn_rcv_form.html'

    def get_success_url(self):
        lc_pk = LCItem.objects.get(id=self.kwargs['lc_item_pk']).lc_id
        return reverse('inv:lc_detailview', args=[lc_pk])

    def form_valid(self, form):
        lc_item_pk = self.kwargs['lc_item_pk']
        form.instance.lc_item = LCItem.objects.get(id=lc_item_pk)
        return super(YarnRcvCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(YarnRcvCreateView, self).get_context_data(**kwargs)
        context['available_quantity'] = LCItem.objects.get(id=self.kwargs['lc_item_pk']).available_to_receive()
        return context


class YarnRcvListView(generic.ListView):
    model = YarnRcv
    template_name = "inv/yarn_rcv_list.html"


class YarnRcvSearchView(generic.FormView):
    template_name = "inv/yarn_rcv_search.html"
    form_class = YarnRcvSearchForm


class YarnRcvSearchResultListView(generic.ListView):
    model = YarnRcv
    template_name = 'inv/yarn_rcv_list.html'

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return YarnRcv.objects.filter(lc_item__lc__number__icontains=query)


class YarnIssueCreateView(generic.CreateView):
    model = YarnIssue
    fields = ['date', 'challan_no', 'style', 'color', 'quantity', 'knitting_factory_name', 'machine_brand', 'machine_dia', 'grey_finished_dia', 'machine_gauge', 'finished_garments_quality']
    template_name = 'inv/yarn_issue_form.html'

    def get_success_url(self):
        return reverse('inv:yarn_issue_listview')

    def form_valid(self, form):
        lc_item_pk = self.kwargs['lc_item_pk']
        form.instance.lc_item = LCItem.objects.get(id=lc_item_pk)
        return super(YarnIssueCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(YarnIssueCreateView, self).get_context_data(**kwargs)
        context['available_quantity'] = LCItem.objects.get(id=self.kwargs['lc_item_pk']).yarn_bal
        return context


class YarnIssueListView(generic.ListView):
    model = YarnIssue
    template_name = 'inv/yarn_issue_list.html'


class YarnIssueSearchView(generic.FormView):
    template_name = 'inv/yarn_issue_search.html'
    form_class = YarnIssueSearchForm


class YarnIssueSearchResultView(generic.ListView):
    model = YarnIssue
    template_name = "inv/yarn_issue_list.html"

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return YarnIssue.objects.filter(lc_item__lc__number__icontains=query)


class FabricDeliveryCreateView(generic.CreateView):
    model = FabricDelivery
    fields = '__all__'
    template_name = "inv/fabrice_delivery_form.html"

    def get_success_url(self):
        return reverse('inv:fabric_delivery_listview')


class FabricDeliveryListView(generic.ListView):
    model = FabricDelivery
    template_name = "inv/fabric_delivery_list.html"


class FabricDeliverySearchView(generic.FormView):
    template_name = 'inv/fabric_delivery_search.html'
    form_class = FabricDeliverySearchForm


class FabricDeliverySearchResultView(generic.ListView):
    model = FabricDelivery
    template_name = "inv/fabric_delivery_list.html"

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return FabricDelivery.objects.filter(style__icontains=query)
