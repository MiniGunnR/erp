from django import forms

from .models import Worksheet, WorksheetRow, Inventory


class WorksheetForm(forms.ModelForm):
    class Meta:
        model = Worksheet
        fields = ['ref_no']


class WorksheetRowForm(forms.ModelForm):
    class Meta:
        model = WorksheetRow
        fields = ['part_no', 'barcode', 'description', 'quantity', 'gram_p_s', 'total', 'per_pcs_duty_tax', 'air_freight_cost_p_pcs', 'net_purchase_price_taka', 'price_after_tax', 'unit_price_in_taka', 'brand', 'total_price_in_taka']


class BillForm(forms.ModelForm):
    class Meta:
        model = Worksheet
        fields = ['ref_no']


class BillRowForm(forms.ModelForm):
    class Meta:
        model = WorksheetRow
        fields = ['part_no', 'quantity', 'unit_price_in_taka', 'total_price_in_taka']


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['part_no', 'brand', 'type', 'description', 'engine_no', 'ship_name', 'serial_no', 'chassis_no', 'cost_price', 'quantity']

