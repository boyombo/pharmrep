from django import forms

from call.models import Call


class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        exclude = ['rep', 'recorded_date']
