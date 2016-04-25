from django import forms

from product.models import Sale, Payment, Rep


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ['recorded_date', 'rep', 'amount']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SaleForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SaleForm, self).clean()
        try:
            Rep.objects.get(user=self.user)
        except Rep.DoesNotExist:
            raise forms.ValidationError('Only reps can make sales')
        return cleaned_data


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['rep', 'recorded_date', 'balance']
