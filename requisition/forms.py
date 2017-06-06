from django import forms

from .models import Requisition, Item


class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ['company', 'issue_date', 'department', 'vendor']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'price']

