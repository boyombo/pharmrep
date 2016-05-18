from django import forms

from activity import models as activity_models
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
        model = activity_models.Call
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
        return activity_models.Call.GOVT


class PrivateCallForm(CallForm):
    def get_call_type(self):
        return activity_models.Call.PRIVATE


class TradeCallForm(CallForm):
    def get_call_type(self):
        return activity_models.Call.TRADE


class CompetitionForm(BaseActivityForm):
    class Meta:
        model = activity_models.Competition
        exclude = ['recorded_date', 'rep']


class ContactForm(BaseActivityForm):
    class Meta:
        model = activity_models.Contact
        fields = ['name', 'phone', 'address']


class MarketForm(BaseActivityForm):
    class Meta:
        model = activity_models.MarketNeed
        fields = ['text', 'recorded_date']


class ConclusionForm(BaseActivityForm):
    class Meta:
        model = activity_models.Conclusion
        fields = ['text', 'recorded_date']


class ItineraryForm(BaseActivityForm):
    class Meta:
        model = activity_models.Itinerary
        fields = ['recorded_date', 'places']


class SummaryForm(BaseActivityForm):
    class Meta:
        model = activity_models.Summary
        fields = ['start_date', 'end_date', 'report']
