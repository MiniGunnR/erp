from datetime import datetime
from decimal import Decimal

from django.shortcuts import render
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Sum

from .models import Worksheet, WorksheetRow, Inventory, Quotation, QuotationRow, Invoice, InvoiceRow, Challan, ChallanRow
from .forms import WorksheetForm, WorksheetRowForm, InventoryForm
from utils.n2w import final


def home(request):
    return render(request, "europarts/home.html")


def inventory_list(request):
    inventory = Inventory.objects.all()
    context = {
        "inventory": inventory,
    }
    return render(request, "europarts/inventory/inventory_list.html", context)


def inventory_create(request):
    form = InventoryForm(request.POST or None)

    if form.is_valid():
        part_no = form.cleaned_data.get('part_no')
        brand = form.cleaned_data.get('brand')
        type = form.cleaned_data.get('type')
        description = form.cleaned_data.get('description')
        quantity = form.cleaned_data.get('quantity')
        cost_price = form.cleaned_data.get('cost_price')

        Inventory.objects.create(part_no=part_no, brand=brand, type=type, description=description, quantity=quantity, cost_price=cost_price)

        return HttpResponseRedirect(reverse('europarts:inventory_create'))

    context = {
        "form": form,
    }
    return render(request, "europarts/inventory/inventory_create.html", context)

def inventory_edit(request, pk):
    inventory = Inventory.objects.get(pk=pk)

    if request.method == "POST":
        form = InventoryForm(request.POST)

        if form.is_valid():
            part_no = form.cleaned_data.get('part_no')
            brand = form.cleaned_data.get('brand')
            type = form.cleaned_data.get('type')
            description = form.cleaned_data.get('description')
            quantity = inventory.quantity
            cost_price = form.cleaned_data.get('cost_price')

            Inventory.objects.filter(pk=inventory.pk).update(part_no=part_no, brand=brand, type=type, description=description, quantity=quantity, cost_price=cost_price)

            return HttpResponseRedirect(reverse('europarts:inventory_edit', args=(pk,)))
        else:
            print('invalid form')
    else:
        form = InventoryForm(instance=inventory)

    context = {
        "form": form,
        "pk": pk,
        "quantity": inventory.quantity,
    }
    return render(request, "europarts/inventory/inventory_edit.html", context)


def inventory_quantity_add(request, pk):
    inventory = Inventory.objects.get(id=pk)

    if request.method == "POST":
        inventory.quantity += abs(int(request.POST.get('added_quantity')))
        inventory.save()
    return HttpResponseRedirect(reverse('europarts:inventory_edit', args=(pk,)))


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

    qt_objs = Quotation.objects.filter(worksheet=worksheet)
    qt_obj = qt_objs.last()
    if qt_obj is not None:
        recipient = qt_obj.recipient
        recipient_address = qt_obj.recipient_address
    else:
        recipient = ''
        recipient_address = ''

    context = {
        "worksheet": worksheet,
        "row_formset": row_formset,
        "pk": pk,
        "recipient": recipient,
        "recipient_address": recipient_address,
    }
    return render(request, "europarts/worksheet/worksheet_edit.html", context)


def quotation_list(request):
    quotations = Quotation.objects.all()
    context = {
        "quotations": quotations,
    }
    return render(request, "europarts/quotation/quotation_list.html", context)


def quotation_create(request, ws_id):
    worksheet = Worksheet.objects.get(id=ws_id)
    qt_objs = Quotation.objects.filter(worksheet=worksheet)

    if request.method == "POST":
        first_obj = qt_objs.last()
        if first_obj is None:
            ref_no = 'EPBD/{id}/{year}'.format(id=worksheet.id, year=datetime.now().year)
        else:
            count = qt_objs.count()
            ref_no = '{ref}-{count}'.format(ref=first_obj.ref_no, count=count)

        quotation = Quotation.objects.create(ref_no=ref_no, worksheet=worksheet, total=0, recipient=request.POST.get('recipient'), recipient_address=request.POST.get('recipient_address'))

        worksheet_rows = WorksheetRow.objects.filter(worksheet=worksheet)
        for item in worksheet_rows:
            QuotationRow.objects.create(quotation=quotation, part_no=item.part_no, brand=item.brand, type=item.type, description=item.description, quantity=item.quantity, sale_price=item.sale_price, total=item.total)

        qr_objs_total = QuotationRow.objects.filter(quotation=quotation).aggregate(Sum('total'))
        quotation.total = qr_objs_total['total__sum']
        print(quotation.total)
        quotation.save()
    return HttpResponseRedirect(reverse('europarts:quotation_details', args=(quotation.id,)))


def quotation_details(request, pk):
    quotation = Quotation.objects.get(id=pk)
    quotation_rows = QuotationRow.objects.filter(quotation=quotation)
    total_in_words = final(quotation.total)
    context = {
        "quotation": quotation,
        "quotation_rows": quotation_rows,
        "now": datetime.now(),
        "total_in_words": total_in_words,
        "pk": pk,
    }
    return render(request, "europarts/quotation/quotation_details.html", context)


def invoice_list(request):
    invoices = Invoice.objects.all()
    context = {
        "invoices": invoices,
    }
    return render(request, "europarts/invoice/invoice_list.html", context)


def invoice_create(request, qt_id):
    quotation = Quotation.objects.get(id=qt_id)
    invoice_objs = Invoice.objects.filter(quotation=quotation)

    if request.method == "POST":
        first_obj = invoice_objs.last()
        if first_obj is None:
            ref_no = 'EPBD/{id}/{year}'.format(id=quotation.id, year=datetime.now().year)
        else:
            count = invoice_objs.count()
            ref_no = '{ref}-{count}'.format(ref=first_obj.ref_no, count=count)

        invoice = Invoice.objects.create(ref_no=ref_no, quotation=quotation, total=quotation.total, total_after_tax=int(round(quotation.total * Decimal(1.085))), recipient=quotation.recipient, recipient_address=quotation.recipient_address)
        challan = Challan.objects.create(ref_no=ref_no, invoice=invoice, recipient=quotation.recipient, recipient_address=quotation.recipient_address)

        quotation_rows = QuotationRow.objects.filter(quotation=quotation)
        for item in quotation_rows:
            InvoiceRow.objects.create(invoice=invoice, part_no=item.part_no, brand=item.brand, type=item.type, description=item.description, quantity=item.quantity, sale_price=item.sale_price, total=item.total)
            ChallanRow.objects.create(challan=challan, part_no=item.part_no, brand=item.brand, type=item.type, description=item.description, quantity=item.quantity)
            inventory = Inventory.objects.get(part_no=item.part_no)
            inventory.quantity -= item.quantity
            inventory.save()

    return HttpResponseRedirect(reverse('europarts:invoice_details', args=(invoice.id,)))


def invoice_details(request, pk):
    invoice = Invoice.objects.get(id=pk)
    invoice_rows = InvoiceRow.objects.filter(invoice=invoice)
    total_in_words = final(invoice.total_after_tax)
    context = {
        "invoice": invoice,
        "invoice_rows": invoice_rows,
        "now": datetime.now(),
        "total_in_words": total_in_words,
        "pk": pk,
        "vat": invoice.total_after_tax - invoice.total,
    }
    return render(request, "europarts/invoice/invoice_details.html", context)


def challan_list(request):
    challans = Challan.objects.all()
    context = {
        "challans": challans,
    }
    return render(request, "europarts/challan/challan_list.html", context)


def challan_details(request, pk):
    challan = Challan.objects.get(id=pk)
    challan_rows = ChallanRow.objects.filter(challan=challan)

    context = {
        "challan": challan,
        "challan_rows": challan_rows,
        "now": datetime.now(),
        "pk": pk,
    }
    return render(request, "europarts/challan/challan_details.html", context)

