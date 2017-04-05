from django.contrib import admin

from .models import Worksheet, WorksheetRow, Inventory, Quotation, QuotationRow, Invoice, InvoiceRow, Challan, ChallanRow

admin.site.register(Worksheet)
admin.site.register(WorksheetRow)
admin.site.register(Inventory)
admin.site.register(Quotation)
admin.site.register(QuotationRow)
admin.site.register(Invoice)
admin.site.register(InvoiceRow)
admin.site.register(Challan)
admin.site.register(ChallanRow)
