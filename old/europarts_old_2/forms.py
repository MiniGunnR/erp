from django import forms

from .models import Product, List, Brand, AutoType, AutoPart


class ListForm(forms.ModelForm):

    class Meta:
        model = List
        fields = ['ref_no']


class ProductCreateForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), initial=Brand.objects.first())
    auto_type = forms.ModelChoiceField(queryset=AutoType.objects.all(), empty_label=None)
    part_no = forms.CharField(max_length=50)
    description = forms.CharField(max_length=255)
    quantity = forms.IntegerField()
    unit = forms.CharField(max_length=20, initial='piece(s)')
    cost_price = forms.IntegerField(required=False)
    selling_price = forms.IntegerField(required=False)


class AddCostPriceForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['auto_part', 'cost_price']
        widgets = {'auto_part': forms.HiddenInput()}


class AddSellingPriceForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['auto_part', 'cost_price', 'selling_price']
        widgets = {'auto_part': forms.HiddenInput(), 'cost_price': forms.HiddenInput()}
