from django.shortcuts import render, reverse
from django.views import generic
from django.db import transaction

from .models import LC, LCItem, YarnRcv

from .forms import LC_Formset, SearchForm


class LCCreateView(generic.CreateView):
  model = LC
  fields = ['date', 'number', 'spinning_mill']
  template_name = 'inv/lc_form.html'

  def get_success_url(self):
    return reverse('inv:lc_updateview', args=[self.object.pk])

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
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
    return super().form_valid(form)


class LCUpdateView(generic.UpdateView):
  model = LC
  fields = ['date', 'number', 'spinning_mill']
  template_name = 'inv/lc_form.html'

  def get_success_url(self):
    return reverse('inv:lc_updateview', args=[self.object.pk])

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
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
    return super().form_valid(form)


class LCListView(generic.ListView):
  model = LC
  template_name = 'inv/lc_list.html'


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
    return super().form_valid(form)


class LCDetailView(generic.DetailView):
  model = LC
  template_name = 'inv/lc_detail.html'


class LCSearchView(generic.FormView):
  template_name = 'inv/lc_search.html'
  form_class = SearchForm


class LCSearchResultListView(generic.ListView):
  model = LC
  template_name = 'inv/lc_list.html'

  def get_queryset(self):
    query = self.request.GET.get('query', '')
    return LC.objects.filter(number__icontains=query)

