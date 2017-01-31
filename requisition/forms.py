from django import forms

from .models import Requisition, Item


class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ['']