from django import forms

from call.models import Call
from product.models import Rep


class CallForm(forms.ModelForm):

    class Meta:
        model = Call
        exclude = ['rep', 'recorded_date', 'call_type']

    def __init__(self, *args, **kwargs):
        #import pdb;pdb.set_trace()
        self.user = kwargs.pop('user')
        super(CallForm, self).__init__(*args, **kwargs)

    def clean(self):
        try:
            self.rep = Rep.objects.get(user=self.user)
        except Rep.DoesNotExist:
            raise forms.ValidationError(
                'Only reps are allowed to make calls')

    def get_call_type(self):
        raise NotImplementedError

    def save(self):
        obj = super(CallForm, self).save(commit=False)
        obj.rep = self.rep
        obj.call_type = self.get_call_type()
        obj.save()


class GovtCallForm(CallForm):
    def get_call_type(self):
        return Call.GOVT


class PrivateCallForm(CallForm):
    def get_call_type(self):
        return Call.PRIVATE


class TradeCallForm(CallForm):
    def get_call_type(self):
        return Call.TRADE
