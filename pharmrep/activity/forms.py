from django import forms

from activity.models import Call, Competition, Contact, MarketNeed, Conclusion
from product.models import Rep


class BaseActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BaseActivityForm, self).__init__(*args, **kwargs)

    def clean(self):
        try:
            self.rep = Rep.objects.get(user=self.user)
        except Rep.DoesNotExist:
            raise forms.ValidationError(
                'Only reps are allowed to perform this activity')


class CallForm(BaseActivityForm):

    class Meta:
        model = Call
        exclude = ['rep', 'recorded_date', 'call_type']

    #def __init__(self, *args, **kwargs):
    #    #import pdb;pdb.set_trace()
    #    self.user = kwargs.pop('user')
    #    super(CallForm, self).__init__(*args, **kwargs)

    #def clean(self):
    #    try:
    #        self.rep = Rep.objects.get(user=self.user)
    #    except Rep.DoesNotExist:
    #        raise forms.ValidationError(
    #            'Only reps are allowed to make calls')

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


class CompetitionForm(BaseActivityForm):
    class Meta:
        model = Competition
        fields = ['activity', 'recorded_date']


class ContactForm(BaseActivityForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'address']


class MarketForm(BaseActivityForm):
    class Meta:
        model = MarketNeed
        fields = ['text', 'recorded_date']


class ConclusionForm(BaseActivityForm):
    class Meta:
        model = Conclusion
        fields = ['text', 'recorded_date']
