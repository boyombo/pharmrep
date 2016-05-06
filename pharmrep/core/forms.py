from datetime import date, timedelta
from django import forms

from product.models import Rep


def sixdaysago():
    return date.today() - timedelta(6)


class SearchForm(forms.Form):
    start = forms.DateField(initial=sixdaysago, required=False)
    end = forms.DateField(initial=date.today, required=False)
    rep = forms.ModelChoiceField(queryset=Rep.objects.all, empty_label='Me')

    def __init__(self, supervisor, *args, **kwargs):
        subordinates = Rep.objects.filter(supervisor=supervisor)
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['rep'] = forms.ModelChoiceField(
            queryset=subordinates,
            empty_label='{} (You)'.format(supervisor.name),
            required=False)
