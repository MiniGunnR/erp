from django import forms


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
