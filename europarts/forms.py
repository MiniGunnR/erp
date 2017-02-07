from django import forms

from .models import Product, List


class ListForm(forms.ModelForm):

    class Meta:
        model = List
        fields = ['ref_no']


# class ProductForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super(ProductForm, self).__init__(*args, **kwargs)
#         self.fields['unit'].initial = 'piece(s)'
#
#     class Meta:
#         model = Product
#         fields = ['description', 'part_no', 'brand', 'quantity', 'unit', 'cost_price', 'selling_price']


class ProductForm(forms.Form):
    part_no = forms.CharField(max_length=50)
    description = forms.CharField(max_length=255)
    brand = forms.CharField(max_length=50)
    quantity = forms.IntegerField()
    unit = forms.CharField(max_length=20, initial='piece(s)')
    cost_price = forms.IntegerField(required=False)
    selling_price = forms.IntegerField(required=False)
