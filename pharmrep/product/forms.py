from django import forms

from product.models import Sale, Payment


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ['recorded_date', 'rep']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['rep', 'recorded_date', 'balance']
