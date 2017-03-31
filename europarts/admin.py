from django.contrib import admin

from .models import Worksheet, WorksheetRow, Inventory

admin.site.register(Worksheet)
admin.site.register(WorksheetRow)
admin.site.register(Inventory)
