from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse
from django.views.generic import DetailView, View
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from wkhtmltopdf.views import PDFTemplateResponse

from .models import Requisition, Item, PurchaseOrder
from .forms import RequisitionForm, ItemForm


def home(request):
    objs = Requisition.objects.all()
    c = {
        "objs": objs,
    }
    return render(request, "requisition/home.html", c)


@login_required
def create_requisition(request):
    ItemFormSet = formset_factory(ItemForm)

    if request.method == "POST":
        requisition_form = RequisitionForm(request.POST)
        item_formset = ItemFormSet(request.POST)

        if requisition_form.is_valid() and item_formset.is_valid():
            company = requisition_form.cleaned_data.get('company')
            issue_date = requisition_form.cleaned_data.get('issue_date')
            department = requisition_form.cleaned_data.get('department')
            vendor = requisition_form.cleaned_data.get('vendor')
            requisition = Requisition.objects.create(company=company, issue_date=issue_date, department=department, vendor=vendor, created_by=request.user, modified_by=request.user)

            new_items = []

            for item_form in item_formset:
                name = item_form.cleaned_data.get('name')
                quantity = item_form.cleaned_data.get('quantity')
                price = item_form.cleaned_data.get('price')
                amount = item_form.cleaned_data.get('amount')

                if name and quantity and price:
                    new_items.append(Item(requisition=requisition, name=name, quantity=quantity, price=price))

            try:
                with transaction.atomic():
                    for item in new_items:
                        item.save()

                    messages.success(request, 'You have created a new requisition.')
                    return HttpResponseRedirect(reverse('requisition:home'))
            except IntegrityError:
                messages.error(request, 'There was an error saving your requisition.')
                return HttpResponseRedirect(reverse('requisition:home'))
    else:
        requisition_form = RequisitionForm()
        item_formset = ItemFormSet()

    c = {
        "requisition_form": requisition_form,
        "item_formset": item_formset,
    }
    return render(request, "requisition/create-requisition.html", c)


@login_required
def edit_requisition(request, pk):
    requisition = Requisition.objects.get(id=pk)

    ItemFormSet = formset_factory(ItemForm, extra=0)

    requisition_items = Item.objects.filter(requisition=requisition)
    requisition_data = {'company': requisition.company, 'issue_date': requisition.issue_date, 'department': requisition.department, 'vendor': requisition.vendor}
    item_data = [{'name': i.name, 'quantity': i.quantity, 'price': i.price} for i in requisition_items]

    if request.method == "POST":
        requisition_form = RequisitionForm(request.POST)
        item_formset = ItemFormSet(request.POST)

        if requisition_form.is_valid() and item_formset.is_valid():
            company = requisition_form.cleaned_data.get('company')
            issue_date = requisition_form.cleaned_data.get('issue_date')
            department = requisition_form.cleaned_data.get('department')
            vendor = requisition_form.cleaned_data.get('vendor')

            requisition.company = company
            requisition.issue_date = issue_date
            requisition.department = department
            requisition.vendor = vendor
            requisition.modified_by = request.user
            requisition.save()

            new_items = []

            for item_form in item_formset:
                name = item_form.cleaned_data.get('name')
                quantity = item_form.cleaned_data.get('quantity')
                price = item_form.cleaned_data.get('price')

                if name and quantity and price:
                    new_items.append(Item(requisition=requisition, name=name, quantity=quantity, price=price))

            try:
                with transaction.atomic():
                    Item.objects.filter(requisition=requisition).delete()
                    for item in new_items:
                        item.save()

                    messages.success(request, 'You have created a new requisition.')
                    return HttpResponseRedirect(reverse('requisition:home'))
            except IntegrityError:
                messages.error(request, 'There was an error saving your requisition.')
                return HttpResponseRedirect(reverse('requisition:home'))
    else:
        requisition_form = RequisitionForm(initial=requisition_data)
        item_formset = ItemFormSet(initial=item_data)

    c = {
        "requisition_form": requisition_form,
        "item_formset": item_formset,
    }
    return render(request, "requisition/edit-requisition.html", c)


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


class RequisitionView(View, LoginRequiredMixin):
    template = "requisition/requisition_template.html"

    def get(self, request, **kwargs):
        req = Requisition.objects.get(pk=kwargs['pk'])
        objs = Item.objects.filter(requisition_id=kwargs['pk'])

        context = {
            "pk": kwargs['pk'],
            "full_name": self.request.user.get_full_name(),
            "requisition": req,
            "items": objs,
        }

        response = PDFTemplateResponse(
            request=request,
            template=self.template,
            filename='requisition.pdf',
            context=context,
            show_content_in_browser=False,
            cmd_options={'margin-top': 10,
                         'zoom': 1,
                         'viewport-size': '1366 x 513',
                         'javascript-delay': 1000,
                         'no-stop-slow-scripts': True}
        )

        return response
