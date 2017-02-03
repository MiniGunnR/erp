from django import forms

from .models import Product, ProductList


class ProductListForm(forms.ModelForm):
    class Meta:
        model = ProductList
        fields = ['ref_no']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['description', 'part_no', 'brand', 'quantity', 'unit']
