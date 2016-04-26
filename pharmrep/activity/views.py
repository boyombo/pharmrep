from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.edit import CreateView

from activity import forms as activity_forms

from product.models import Rep
from activity.models import Call, Competition


@method_decorator(login_required, name='dispatch')
class BaseActivityCreateView(CreateView):
    model = None
    success_msg = None
    success_url = None

    def get_form_kwargs(self):
        kwargs = super(BaseActivityCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.rep = Rep.objects.get(user=self.request.user)
        obj.save()
        messages.success(self.request, self.success_msg)
        return super(BaseActivityCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class CallView(BaseActivityCreateView):
    model = Call
    success_msg = 'Successfully added call'
    success_url = '/activity/govt/'

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super(BaseActivityCreateView, self).form_valid(form)


class GovtCallView(CallView):
    template_name = 'activity/govt.html'
    form_class = activity_forms.GovtCallForm
    success_url = '/activity/govt/'


class PrivateCallView(CallView):
    template_name = 'activity/private.html'
    form_class = activity_forms.PrivateCallForm
    success_url = '/activity/private/'


class TradeCallView(CallView):
    template_name = 'activity/trade.html'
    form_class = activity_forms.TradeCallForm
    success_url = '/activity/trade/'


@login_required
def call_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    calls = Call.objects.filter(rep=rep).order_by('-call_date')
    return render(request, 'activity/calls_list.html', {'calls': calls})


class CompetitionView(BaseActivityCreateView):
    template_name = 'activity/competition.html'
    form_class = activity_forms.CompetitionForm
    success_url = '/activity/competition/'
    success_msg = 'Successfully added competitor activity'


@login_required
def competition_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    activities = Competition.objects.filter(rep=rep).order_by(
        '-recorded_date')
    return render(request, 'activity/competition_list.html',
                  {'acts': activities})
