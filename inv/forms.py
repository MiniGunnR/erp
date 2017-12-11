# from django import forms
#
# from .models import LetterOfCredit, LCItem, FabricDelivery
#
#
# class QuantityForm(forms.Form):
#     quantity = forms.IntegerField()
#
#     def clean(self):
#         cleaned_data = super(QuantityForm, self).clean()
#         quantity = cleaned_data.get("quantity")
#
#         if quantity:
#             if quantity < 1:
#                 raise forms.ValidationError(
#                     "Value must be positive."
#                 )
#
#
# class LetterOfCreditForm(forms.ModelForm):
#     class Meta:
#         model = LetterOfCredit
#         fields = ['date', 'number', 'spinning_mill']
#
#
# class LCItemForm(forms.ModelForm):
#     class Meta:
#         model = LCItem
#         fields = ['count', 'item', 'quantity', 'unit', 'style_no', 'color']
#
# LC_Formset = forms.inlineformset_factory(LetterOfCredit, LCItem, form=LCItemForm, extra=1)
#
#
# class LcSearchForm(forms.Form):
#     q = forms.IntegerField(label="LC")
#
#
# class YrSearchForm(forms.Form):
#     q = forms.CharField(label="Barcode")
#
#
# class YiSearchForm(forms.Form):
#     q = forms.CharField(label="Barcode")
#
#
# class FdSearchForm(forms.Form):
#     q = forms.CharField(label="Barcode")
#
#
# class FdForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(FdForm, self).__init__(*args, **kwargs)
#         self.fields['open_dia'].widget.attrs = {
#             'class': 'filled-in',
#         }
#         self.fields['tube_dia'].widget.attrs = {
#             'class': 'filled-in',
#         }
#
#     class Meta:
#         model = FabricDelivery
#         fields = ['yd', 'date', 'barcode', 'fabric_type', 'colour', 'dia_name', 'fabric_construction', 'received_grey_dia', 'finished_fabric_dia', 'finished_fabric_gsm', 'stitch_length', 'stitch_color', 'open_dia', 'tube_dia']
