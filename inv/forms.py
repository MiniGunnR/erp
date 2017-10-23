from django import forms

from .models import LetterOfCredit, LCItem


class QuantityForm(forms.Form):
    quantity = forms.IntegerField()

    def clean(self):
        cleaned_data = super(QuantityForm, self).clean()
        quantity = cleaned_data.get("quantity")

        if quantity:
            if quantity < 1:
                raise forms.ValidationError(
                    "Value must be positive."
                )


class LetterOfCreditForm(forms.ModelForm):
    class Meta:
        model = LetterOfCredit
        fields = ['date', 'number', 'spinning_mill']


class LCItemForm(forms.ModelForm):
    class Meta:
        model = LCItem
        fields = ['count', 'item', 'quantity']

LC_Formset = forms.inlineformset_factory(LetterOfCredit, LCItem, form=LCItemForm, extra=1)


class LcSearchForm(forms.Form):
    q = forms.IntegerField(label="LC")


class YrSearchForm(forms.Form):
    q = forms.CharField(label="Barcode")


class YdSearchForm(forms.Form):
    q = forms.CharField(label="Barcode")


class FdSearchForm(forms.Form):
    q = forms.CharField(label="Barcode")
