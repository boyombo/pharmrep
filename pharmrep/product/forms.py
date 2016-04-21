from django import forms

from product.models import Sale


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ['recorded_date']
