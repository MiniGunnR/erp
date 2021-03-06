from datetime import datetime
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from django.shortcuts import render
from django.views import generic
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.core.mail import EmailMessage

from .models import Worksheet, WorksheetRow, Inventory, Quotation, QuotationRow, Invoice, InvoiceRow, Challan, \
    ChallanRow, Client, Job, Option
from .forms import WorksheetForm, WorksheetRowForm, InventoryForm, BillRowForm, BillForm
from europarts.tasks import generate_pdf_and_send_email
from core.models import Mail

from utils.mixins import AtomicMixin
from utils.n2w import final
from utils.func import is_member


@login_required
def home(request):
    return render(request, "europarts/home.html")


@login_required
def inventory_list(request):
    inventory = Inventory.objects.all()
    context = {
        "inventory": inventory,
    }
    return render(request, "europarts/inventory/inventory_list.html", context)


@login_required
def inventory_create(request):
    form = InventoryForm(request.POST or None)

    if form.is_valid():
        part_no = form.cleaned_data.get('part_no')
        barcode = form.cleaned_data.get('barcode')
        brand = form.cleaned_data.get('brand')
        type = form.cleaned_data.get('type')
        description = form.cleaned_data.get('description')
        engine_no = form.cleaned_data.get('engine_no')
        ship_name = form.cleaned_data.get('ship_name')
        serial_no = form.cleaned_data.get('serial_no')
        chassis_no = form.cleaned_data.get('chassis_no')
        quantity = form.cleaned_data.get('quantity')
        cost_price = form.cleaned_data.get('cost_price')

        Inventory.objects.create(part_no=part_no,
                                 barcode=barcode,
                                 brand=brand,
                                 type=type,
                                 description=description,
                                 engine_no=engine_no,
                                 ship_name=ship_name,
                                 serial_no=serial_no,
                                 chassis_no=chassis_no,
                                 quantity=quantity,
                                 cost_price=cost_price)

        return HttpResponseRedirect(reverse('europarts:inventory_create'))

    context = {
        "form": form,
    }
    return render(request, "europarts/inventory/inventory_create.html", context)


@login_required
def inventory_edit(request, pk):
    inventory = Inventory.objects.get(pk=pk)

    if request.method == "POST":
        form = InventoryForm(request.POST)

        if form.is_valid():
            part_no = form.cleaned_data.get('part_no')
            barcode = form.cleaned_data.get('barcode')
            brand = form.cleaned_data.get('brand')
            type = form.cleaned_data.get('type')
            description = form.cleaned_data.get('description')
            engine_no = form.cleaned_data.get('engine_no')
            ship_name = form.cleaned_data.get('ship_name')
            serial_no = form.cleaned_data.get('serial_no')
            chassis_no = form.cleaned_data.get('chassis_no')
            quantity = inventory.quantity
            cost_price = form.cleaned_data.get('cost_price')

            Inventory.objects.filter(pk=inventory.pk).update(part_no=part_no,
                                                             barcode=barcode,
                                                             brand=brand,
                                                             type=type,
                                                             description=description,
                                                             engine_no=engine_no,
                                                             ship_name=ship_name,
                                                             serial_no=serial_no,
                                                             chassis_no=chassis_no,
                                                             quantity=quantity,
                                                             cost_price=cost_price)

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


@login_required
def inventory_quantity_add(request, pk):
    inventory = Inventory.objects.get(id=pk)

    if request.method == "POST":
        inventory.quantity += abs(int(request.POST.get('added_quantity')))
        inventory.save()
    return HttpResponseRedirect(reverse('europarts:inventory_edit', args=(pk,)))


@login_required
def worksheet_list(request):
    worksheets = Worksheet.objects.all()
    context = {
        "worksheets": worksheets,
    }
    return render(request, "europarts/worksheet/worksheet_list.html", context)


@login_required
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
                barcode = row_form.cleaned_data.get('part_no')
                description = row_form.cleaned_data.get('description')
                quantity = row_form.cleaned_data.get('quantity')
                gram_p_s = row_form.cleaned_data.get('gram_p_s')
                total = row_form.cleaned_data.get('total')
                per_pcs_duty_tax = row_form.cleaned_data.get('per_pcs_duty_tax')
                air_freight_cost_p_pcs = row_form.cleaned_data.get('air_freight_cost_p_pcs')
                net_purchase_price_taka = row_form.cleaned_data.get('net_purchase_price_taka')
                tax = row_form.cleaned_data.get('tax')
                price_after_tax = row_form.cleaned_data.get('price_after_tax')
                unit_price_in_taka = row_form.cleaned_data.get('unit_price_in_taka')
                brand = row_form.cleaned_data.get('brand')
                vat = row_form.cleaned_data.get('vat')
                total_price_in_taka = row_form.cleaned_data.get('total_price_in_taka')

                if part_no is not None:
                    WorksheetRow.objects.create(
                        worksheet=worksheet,
                        part_no=part_no,
                        barcode=barcode,
                        description=description,
                        quantity=quantity,
                        gram_p_s=gram_p_s,
                        total=total,
                        per_pcs_duty_tax=per_pcs_duty_tax,
                        air_freight_cost_p_pcs=air_freight_cost_p_pcs,
                        net_purchase_price_taka=net_purchase_price_taka,
                        tax=tax,
                        price_after_tax=price_after_tax,
                        unit_price_in_taka=unit_price_in_taka,
                        brand=brand,
                        vat=vat,
                        total_price_in_taka=total_price_in_taka,
                        )

            return HttpResponseRedirect(reverse('europarts:worksheet_edit', args=(worksheet.pk,)))
    else:
        worksheet_form = WorksheetForm()
        row_formset = WorksheetRowFormset()
    context = {
        "worksheet_form": worksheet_form,
        "row_formset": row_formset,
    }
    return render(request, "europarts/worksheet/worksheet_create.html", context)


@login_required
def worksheet_edit(request, pk):
    row_qs = WorksheetRow.objects.filter(worksheet_id=pk)
    count = row_qs.count()
    extra = 100 - count

    WorksheetRowFormset = formset_factory(WorksheetRowForm, extra=extra)

    worksheet = Worksheet.objects.get(id=pk)

    old_rows = WorksheetRow.objects.filter(worksheet=worksheet)
    row_data = [{
        'part_no': row.part_no,
        'barcode': row.barcode,
        'description': row.description,
        'quantity': row.quantity,
        'gram_p_s': row.gram_p_s,
        'total': row.total,
        'per_pcs_duty_tax': row.per_pcs_duty_tax,
        'air_freight_cost_p_pcs': row.air_freight_cost_p_pcs,
        'net_purchase_price_taka': row.net_purchase_price_taka,
        'tax': row.tax,
        'price_after_tax': row.price_after_tax,
        'unit_price_in_taka': row.unit_price_in_taka,
        'brand': row.brand,
        'vat': row.vat,
        'total_price_in_taka': row.total_price_in_taka,
                } for row in old_rows]

    if request.method == "POST":
        row_formset = WorksheetRowFormset(request.POST)

        if row_formset.is_valid():
            print('formset valid')
            WorksheetRow.objects.filter(worksheet=worksheet).delete()

            for row_form in row_formset:
                print('row_form')
                part_no = row_form.cleaned_data.get('part_no')
                barcode = row_form.cleaned_data.get('barcode')
                description = row_form.cleaned_data.get('description')
                quantity = row_form.cleaned_data.get('quantity')
                gram_p_s = row_form.cleaned_data.get('gram_p_s')
                total = row_form.cleaned_data.get('total')
                per_pcs_duty_tax = row_form.cleaned_data.get('per_pcs_duty_tax')
                air_freight_cost_p_pcs = row_form.cleaned_data.get('air_freight_cost_p_pcs')
                net_purchase_price_taka = row_form.cleaned_data.get('net_purchase_price_taka')
                tax = row_form.cleaned_data.get('tax')
                price_after_tax = row_form.cleaned_data.get('price_after_tax')
                unit_price_in_taka = row_form.cleaned_data.get('unit_price_in_taka')
                brand = row_form.cleaned_data.get('brand')
                vat = row_form.cleaned_data.get('vat')
                total_price_in_taka = row_form.cleaned_data.get('total_price_in_taka')
                if part_no is not None:
                    print('worksheet being created')
                    WorksheetRow.objects.create(
                        worksheet=worksheet,
                        part_no=part_no,
                        barcode=barcode,
                        description=description,
                        quantity=quantity,
                        gram_p_s=gram_p_s,
                        total=total,
                        per_pcs_duty_tax=per_pcs_duty_tax,
                        air_freight_cost_p_pcs=air_freight_cost_p_pcs,
                        net_purchase_price_taka=net_purchase_price_taka,
                        tax=tax,
                        price_after_tax=price_after_tax,
                        unit_price_in_taka=unit_price_in_taka,
                        brand=brand,
                        vat=vat,
                        total_price_in_taka=total_price_in_taka,
                        )
                    print('worksheet created')

            return HttpResponseRedirect(reverse('europarts:worksheet_edit', args=(pk,)))
    else:
        row_formset = WorksheetRowFormset(initial=row_data)

    qt_objs = Quotation.objects.filter(worksheet=worksheet)
    qt_obj = qt_objs.last()
    if qt_obj is not None:
        recipient = qt_obj.client.name
        recipient_address = qt_obj.client.address
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


@login_required
def bill_list(request):
    worksheets = Worksheet.objects.all()
    context = {
        "worksheets": worksheets,
    }
    return render(request, "europarts/bill/bill_list.html", context)


@login_required
@transaction.atomic
def bill_create(request):
    BillRowFormset = formset_factory(BillRowForm, extra=1)

    if request.method == "POST":
        bill_form = BillForm(request.POST)
        row_formset = BillRowFormset(request.POST)

        if bill_form.is_valid() and row_formset.is_valid():
            ref_no = bill_form.cleaned_data.get('ref_no')
            worksheet = Worksheet.objects.create(ref_no=ref_no)

            for row_form in row_formset:
                part_no = row_form.cleaned_data.get('part_no')
                quantity = row_form.cleaned_data.get('quantity')
                unit_price_in_taka = row_form.cleaned_data.get('unit_price_in_taka')
                total_price_in_taka = row_form.cleaned_data.get('total_price_in_taka')

                if part_no is not None:
                    inventory, created = Inventory.objects.get_or_create(
                        part_no=part_no,
                        defaults={
                            'quantity': quantity,
                            'cost_price': unit_price_in_taka,
                        }
                    )

                    WorksheetRow.objects.create(
                        worksheet=worksheet,
                        part_no=part_no,
                        quantity=quantity,
                        unit_price_in_taka=unit_price_in_taka,
                        total_price_in_taka=total_price_in_taka,
                    )
            return HttpResponseRedirect(reverse('europarts:bill_edit', args=(worksheet.pk,)))
    else:
        bill_form = BillForm()
        row_formset = BillRowFormset()
    context = {
        "bill_form": bill_form,
        "row_formset": row_formset,
    }
    return render(request, "europarts/bill/bill_create.html", context)


@login_required
@transaction.atomic
def bill_edit(request, pk):
    all_rows = WorksheetRow.objects.filter(worksheet_id=pk)

    BillRowFormset = formset_factory(BillRowForm, extra=0)

    worksheet = Worksheet.objects.get(id=pk)

    old_rows = WorksheetRow.objects.filter(worksheet=worksheet)
    row_data = [{'part_no': row.part_no,
                 'quantity': row.quantity,
                 'unit_price_in_taka': row.unit_price_in_taka,
                 'total_price_in_taka': row.total_price_in_taka}
                for row in old_rows]
    clients = Client.objects.all()

    if request.method == "POST":
        row_formset = BillRowFormset(request.POST)

        if row_formset.is_valid():
            all_rows.delete()

            for row_form in row_formset:
                part_no = row_form.cleaned_data.get('part_no')
                quantity = row_form.cleaned_data.get('quantity')
                unit_price_in_taka = row_form.cleaned_data.get('unit_price_in_taka')
                total_price_in_taka = row_form.cleaned_data.get('total_price_in_taka')

                if part_no is not None:
                    WorksheetRow.objects.create(
                        worksheet=worksheet,
                        part_no=part_no,
                        quantity=quantity,
                        unit_price_in_taka=unit_price_in_taka,
                        total_price_in_taka=total_price_in_taka,
                    )
            return HttpResponseRedirect(reverse('europarts:bill_edit', args=(pk,)))
    else:
        row_formset = BillRowFormset(initial=row_data)

    context = {
        "worksheet": worksheet,
        "row_formset": row_formset,
        "pk": pk,
        "clients": clients
    }
    return render(request, "europarts/bill/bill_edit.html", context)


@login_required
def quotation_list(request):
    quotations = Quotation.objects.all()
    context = {
        "quotations": quotations,
    }
    return render(request, "europarts/quotation/quotation_list.html", context)


@login_required
@transaction.atomic
def quotation_create(request, ws_id):
    worksheet = Worksheet.objects.get(id=ws_id)
    qt_objs = Quotation.objects.filter(worksheet=worksheet)

    if request.method == "POST":
        print(request.POST)
        first_obj = qt_objs.last()

        # generate display_id that increases by 5
        # try:
        #     quotation = Quotation.objects.order_by('created').last()
        #     display_id = quotation.display_id
        # except:
        #     display_id = 5
        # else:
        #     if worksheet.id == quotation.worksheet_id:
        #         display_id = quotation.display_id
        #     else:
        #         display_id = int(display_id) + 5

        if first_obj is None:
            # ref_no = 'EPBD/{id}/{year}'.format(id=worksheet.id, year=datetime.now().year)
            ref_no = 'EPBD/{id}/{year}'.format(id=worksheet.display_id, year=datetime.now().year)
        else:
            count = qt_objs.count()
            # ref_no = '{ref}-{count}'.format(ref=first_obj.ref_no, count=count)
            # ref_no = 'EPBD/{id}-{count}/{year}'.format(id=worksheet.id, count=count, year=datetime.now().year)
            ref_no = 'EPBD/{id}-{count}/{year}'.format(id=worksheet.display_id, count=count, year=datetime.now().year)

        # quotation = Quotation.objects.create(ref_no=ref_no, worksheet=worksheet, total=0, recipient=request.POST.get('recipient'), recipient_address=request.POST.get('recipient_address'))
        quotation = Quotation.objects.create(ref_no=ref_no, worksheet=worksheet, total=0, client_id=request.POST.get('client'))

        worksheet_rows = WorksheetRow.objects.filter(worksheet=worksheet)
        for item in worksheet_rows:
            # QuotationRow.objects.create(quotation=quotation, part_no=item.part_no, brand=item.brand, type=item.type, description=item.description, quantity=item.quantity, sale_price=item.sale_price, total=item.total)
            QuotationRow.objects.create(quotation=quotation, part_no=item.part_no, quantity=item.quantity, sale_price=item.unit_price_in_taka, total=item.total_price_in_taka)

        qr_objs_total = QuotationRow.objects.filter(quotation=quotation).aggregate(Sum('total'))
        quotation.total = qr_objs_total['total__sum']
        print(quotation.total)
        quotation.save()
    return HttpResponseRedirect(reverse('europarts:quotation_details', args=(quotation.id,)))


@login_required
def quotation_details(request, pk):
    quotation = Quotation.objects.get(id=pk)
    quotation_rows = QuotationRow.objects.filter(quotation=quotation)
    total_in_words = final(quotation.total)
    context = {
        "quotation": quotation,
        "quotation_rows": quotation_rows,
        "now": quotation.created,
        "total_in_words": total_in_words,
        "pk": pk,
    }
    return render(request, "europarts/quotation/quotation_details.html", context)


class QuotationEmail(AtomicMixin, View, LoginRequiredMixin):
    template = "europarts/quotation/email_template.html"

    def get(self, request, **kwargs):
        quotation = Quotation.objects.get(pk=kwargs['pk'])
        ref_no = quotation.ref_no
        date = quotation.created.strftime("%b %d, %Y")
        recipient = quotation.recipient
        address = quotation.recipient_address
        total = quotation.total
        total_in_words = final(total)

        context = {
            "ref_no": ref_no,
            "date": date,
            "recipient": recipient,
            "address": address,
            "total": total,
            "total_in_words": total_in_words,
        }

        subject = 'From Design Ace Limited'
        body = self.request.GET['email_body']
        body = body.strip()
        if not body:
            body = 'Dear Sir,\n\nPlease find the attached file.\n\nSincerely yours,\nMd Sorower Hossain'
        from_email = 'Sorower Hossain <sorower@europartsbd.com>'
        to = ['{}'.format(self.request.GET.get('to_address'))]

        # task
        # generate_pdf_and_send_email.delay(self.template, context, self.kwargs['pk'], 'quotation', subject, body, from_email, to)
        generate_pdf_and_send_email(self.template, context, self.kwargs['pk'], 'quotation', subject, body, from_email, to)
            
        # sent mail save with contenttype
        # Mail.objects.create(
        #     owner           = self.request.user,
        #     to_email        = self.request.GET.get('to_address'),
        #     from_email      = from_email,
        #     subject         = subject,
        #     content_object  = quotation,
        #     body            = body,
        # )

        return HttpResponseRedirect(reverse('europarts:quotation_details', args=(kwargs['pk'],)))


@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()
    context = {
        "invoices": invoices,
    }
    return render(request, "europarts/invoice/invoice_list.html", context)


@login_required
@transaction.atomic
def invoice_create(request, qt_id):
    quotation = Quotation.objects.get(id=qt_id)
    invoice_objs = Invoice.objects.filter(quotation=quotation)

    if request.method == "POST":
        first_obj = invoice_objs.last()
        if first_obj is None:
            ref_no = 'EPBD/{id}/{year}'.format(id=quotation.worksheet.display_id, year=datetime.now().year)
        else:
            count = invoice_objs.count()
            ref_no = 'EPBD/{id}-{count}/{year}'.format(id=quotation.worksheet.display_id, count=count, year=datetime.now().year)

        # invoice = Invoice.objects.create(ref_no=ref_no, quotation=quotation, total=quotation.total, total_after_tax=int(round(quotation.total * Decimal(1.085))), recipient=quotation.recipient, recipient_address=quotation.recipient_address)
        invoice = Invoice.objects.create(ref_no=ref_no, quotation=quotation, total=quotation.total, total_after_tax=int(round(quotation.total * Decimal(1.085))), client=quotation.client)
        # challan = Challan.objects.create(ref_no=ref_no, invoice=invoice, recipient=quotation.recipient, recipient_address=quotation.recipient_address)
        challan = Challan.objects.create(ref_no=ref_no, invoice=invoice, client=quotation.client)

        quotation_rows = QuotationRow.objects.filter(quotation=quotation)
        for item in quotation_rows:
            InvoiceRow.objects.create(invoice=invoice, part_no=item.part_no, brand=item.brand, type=item.type, description=item.description, quantity=item.quantity, sale_price=item.sale_price, total=item.total)
            ChallanRow.objects.create(challan=challan, part_no=item.part_no, brand=item.brand, type=item.type, description=item.description, quantity=item.quantity)
            inventory = Inventory.objects.get(part_no=item.part_no)
            inventory.quantity -= item.quantity
            inventory.save()

    return HttpResponseRedirect(reverse('europarts:invoice_details', args=(invoice.id,)))


@login_required
def invoice_details(request, pk):
    invoice = Invoice.objects.get(id=pk)
    invoice_rows = InvoiceRow.objects.filter(invoice=invoice)
    total_in_words = final(invoice.total_after_tax)
    context = {
        "invoice": invoice,
        "invoice_rows": invoice_rows,
        "now": invoice.created,
        "total_in_words": total_in_words,
        "pk": pk,
        "vat": invoice.total_after_tax - invoice.total,
        "paid": invoice.paid
    }
    return render(request, "europarts/invoice/invoice_details.html", context)


class InvoiceEmail(AtomicMixin, View, LoginRequiredMixin):
    template = "europarts/invoice/email_template.html"

    def get(self, request, **kwargs):
        invoice = Invoice.objects.get(pk=kwargs['pk'])
        ref_no = invoice.ref_no
        date = invoice.created.strftime("%b %d, %Y")
        recipient = invoice.recipient
        address = invoice.recipient_address
        total = invoice.total
        vat = float(total) * 0.085
        total_after_tax = float(total) + vat
        total_in_words = final(total)

        context = {
            "ref_no": ref_no,
            "date": date,
            "recipient": recipient,
            "address": address,
            "total": total,
            "vat": vat,
            "total_after_tax": total_after_tax,
            "total_in_words": total_in_words,
        }

        subject = 'From Design Ace Limited'
        body = self.request.GET['email_body']
        body = body.strip()
        if not body:
            body = 'Dear Sir,\n\nPlease find the attached file.\n\nSincerely yours,\nMd Sorower Hossain'
        from_email = 'Sorower Hossain <sorower@europartsbd.com>'
        to = ['{}'.format(self.request.GET.get('to_address'))]

        # task
        # generate_pdf_and_send_email.delay(self.template, context, self.kwargs['pk'], 'invoice', subject, body, from_email, to)
        generate_pdf_and_send_email(self.template, context, self.kwargs['pk'], 'invoice', subject, body, from_email, to)

        # sent mail save with contenttype
        # Mail.objects.create(
        #     owner           = self.request.user,
        #     to_email        = self.request.GET.get('to_address'),
        #     from_email      = from_email,
        #     subject         = subject,
        #     content_object  = invoice,
        #     body            = body,
        # )

        return HttpResponseRedirect(reverse('europarts:invoice_details', args=(kwargs['pk'],)))


class MarkAsPaid(generic.UpdateView):
    model = Invoice
    fields = []
    template_name = 'europarts/invoice/mark_as_paid.html'

    def form_valid(self, form):
        form.instance.paid = True
        return super(MarkAsPaid, self).form_valid(form)

    def get_success_url(self):
        return reverse('europarts:invoice_details', args=[self.kwargs['pk']],)


@login_required
def challan_list(request):
    challans = Challan.objects.all()
    context = {
        "challans": challans,
    }
    return render(request, "europarts/challan/challan_list.html", context)


@login_required
def challan_details(request, pk):
    challan = Challan.objects.get(id=pk)
    challan_rows = ChallanRow.objects.filter(challan=challan)

    context = {
        "challan": challan,
        "challan_rows": challan_rows,
        "now": challan.created,
        "pk": pk,
    }
    return render(request, "europarts/challan/challan_details.html", context)


class ChallanEmail(AtomicMixin, View, LoginRequiredMixin):
    template = "europarts/challan/email_template.html"

    def get(self, request, **kwargs):
        challan = Challan.objects.get(pk=kwargs['pk'])
        ref_no = challan.ref_no
        date = challan.created.strftime("%b %d, %Y")
        recipient = challan.recipient
        address = challan.recipient_address

        context = {
            "ref_no": ref_no,
            "date": date,
            "recipient": recipient,
            "address": address,
        }

        subject = 'From Design Ace Limited'
        body = self.request.GET['email_body']
        body = body.strip()
        if not body:
            body = 'Dear Sir,\n\nPlease find the attached file.\n\nSincerely yours,\nMd Sorower Hossain'
        from_email = 'Sorower Hossain <sorower@europartsbd.com>'
        to = ['{}'.format(self.request.GET.get('to_address'))]

        # task
        # generate_pdf_and_send_email.delay(self.template, context, self.kwargs['pk'], 'challan', subject, body, from_email, to)
        generate_pdf_and_send_email(self.template, context, self.kwargs['pk'], 'challan', subject, body, from_email, to)

        # sent mail save with contenttype
        # Mail.objects.create(
        #     owner           = self.request.user,
        #     to_email        = self.request.GET.get('to_address'),
        #     from_email      = from_email,
        #     subject         = subject,
        #     content_object  = challan,
        #     body            = body,
        # )

        return HttpResponseRedirect(reverse('europarts:challan_details', args=(kwargs['pk'],)))


class ClientListView(generic.ListView):
    model = Client
    template_name = 'europarts/clients/client_list.html'


class ClientCreateView(generic.CreateView):
    model = Client
    fields = ['name', 'address']
    template_name = 'europarts/clients/client_form.html'

    def get_success_url(self):
        return reverse('europarts:clients_list')


class ClientUpdateView(generic.UpdateView):
    model = Client
    fields = ['name', 'address']
    template_name = 'europarts/clients/client_form.html'

    def get_success_url(self):
        return reverse('europarts:clients_list')


class ClientTransactions(generic.ListView):
    model = Invoice
    template_name = 'europarts/clients/client_transactions.html'

    def get_queryset(self):
        return Invoice.objects.filter(client_id=self.kwargs['pk'])


class JobListView(generic.ListView):
    model = Job
    template_name = 'europarts/jobs/job_list.html'

    def get_queryset(self):
        if not is_member(self.request.user, 'EuropartsAdmin'):
            return Job.objects.filter(user=self.request.user)
        return Job.objects.all()


class JobCreateView(generic.CreateView):
    model = Job
    fields = ['appointment_date', 'client_name', 'client_address', 'subject', 'body']
    template_name = 'europarts/jobs/job_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('europarts:jobs_list')


class JobUpdateView(generic.UpdateView):
    model = Job
    fields = ['appointment_date', 'client_name', 'client_address', 'subject', 'body']
    template_name = 'europarts/jobs/job_form.html'

    def get_success_url(self):
        return reverse('europarts:jobs_list')


class JobDetailView(generic.DetailView):
    model = Job
    template_name = 'europarts/jobs/job_detail.html'


def jobs_info_email(request, pk):
    job = Job.objects.get(id=pk)
    to = Option.objects.get(title='job_report_email').value

    subject = job.subject
    body = """Created by: {username}
{job_no}
Created on : {created}
Appointment date : {appointment_date}
Client Name : {client_name}
Client Address : {client_address}

Report : {body}
    """.format(
        username=job.user,
        job_no=job.job_no,
        created=job.created,
        appointment_date=job.appointment_date.strftime("%B %d, %Y"),
        client_name=job.client_name,
        client_address=job.client_address,
        body=job.body
    )
    from_email = request.user.email
    to = [to]

    email = EmailMessage()
    email.subject = "Job Report : {subject}".format(subject=subject)
    email.body = body
    email.from_email = from_email
    email.to = to

    email.send()

    return HttpResponseRedirect(reverse('europarts:jobs_detail', args=[pk, ]))
