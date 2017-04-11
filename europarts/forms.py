from django import forms

from .models import Worksheet, WorksheetRow, Inventory


class WorksheetForm(forms.ModelForm):
    class Meta:
        model = Worksheet
        fields = ['ref_no']


class WorksheetRowForm(forms.ModelForm):
    class Meta:
        model = WorksheetRow
        fields = ['part_no', 'brand', 'type', 'description', 'quantity', 'cost_price', 'sale_price', 'profit_margin', 'total']


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['part_no', 'brand', 'type', 'description', 'cost_price', 'quantity']

