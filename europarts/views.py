from django.shortcuts import render
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Worksheet, WorksheetRow
from .forms import WorksheetForm, WorksheetRowForm


def home(request):
    return render(request, "europarts/home.html")


def worksheet_list(request):
    worksheets = Worksheet.objects.all()
    context = {
        "worksheets": worksheets,
    }
    return render(request, "europarts/worksheet/worksheet_list.html", context)


def worksheet_create(request):
    WorksheetRowFormset = formset_factory(WorksheetRowForm, extra=100)

    if request.method == "POST":
        worksheet_form = WorksheetForm(request.POST)
        row_formset = WorksheetRowFormset(request.POST)

        if worksheet_form.is_valid() and row_formset.is_valid():
            ref_no = worksheet_form.cleaned_data.get('ref_no')
            worksheet = Worksheet.objects.create(ref_no=ref_no)

            for row_form in row_formset:
                part_no = row_form.cleaned_data.get('part_no')
                brand = row_form.cleaned_data.get('brand')
                type = row_form.cleaned_data.get('type')
                description = row_form.cleaned_data.get('description')
                quantity = row_form.cleaned_data.get('quantity')
                cost_price = row_form.cleaned_data.get('cost_price')
                sale_price = row_form.cleaned_data.get('sale_price')
                total = row_form.cleaned_data.get('total')
                if part_no is not None:
                    WorksheetRow.objects.create(worksheet=worksheet, part_no=part_no, brand=brand, type=type, description=description, quantity=quantity, cost_price=cost_price, sale_price=sale_price, total=total)

            return HttpResponseRedirect(reverse('europarts:worksheet_edit', args=(worksheet.pk,)))
    else:
        worksheet_form = WorksheetForm()
        row_formset = WorksheetRowFormset()
    context = {
        "worksheet_form": worksheet_form,
        "row_formset": row_formset,
    }
    return render(request, "europarts/worksheet/worksheet_create.html", context)


def worksheet_edit(request, pk):
    row_qs = WorksheetRow.objects.filter(worksheet_id=pk)
    count = row_qs.count()
    extra = 100 - count

    WorksheetRowFormset = formset_factory(WorksheetRowForm, extra=extra)

    worksheet = Worksheet.objects.get(id=pk)

    old_rows = WorksheetRow.objects.filter(worksheet=worksheet)
    row_data = [{'part_no': row.part_no, 'brand': row.brand, 'type': row.type, 'description': row.description, 'quantity': row.quantity, 'cost_price': row.cost_price, 'sale_price': row.sale_price, 'total': row.total } for row in old_rows]

    if request.method == "POST":
        row_formset = WorksheetRowFormset(request.POST)

        if row_formset.is_valid():
            WorksheetRow.objects.filter(worksheet=worksheet).delete()

            for row_form in row_formset:
                part_no = row_form.cleaned_data.get('part_no')
                brand = row_form.cleaned_data.get('brand')
                type = row_form.cleaned_data.get('type')
                description = row_form.cleaned_data.get('description')
                quantity = row_form.cleaned_data.get('quantity')
                cost_price = row_form.cleaned_data.get('cost_price')
                sale_price = row_form.cleaned_data.get('sale_price')
                total = row_form.cleaned_data.get('total')
                if part_no is not None:
                    WorksheetRow.objects.create(worksheet=worksheet, part_no=part_no, brand=brand, type=type, description=description, quantity=quantity, cost_price=cost_price, sale_price=sale_price, total=total)

            return HttpResponseRedirect(reverse('europarts:worksheet_edit', args=(pk,)))
    else:
        row_formset = WorksheetRowFormset(initial=row_data)
    context = {
        "worksheet": worksheet,
        "row_formset": row_formset,
    }
    return render(request, "europarts/worksheet/worksheet_edit.html", context)


