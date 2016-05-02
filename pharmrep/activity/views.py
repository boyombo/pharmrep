from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.db.models.aggregates import Sum

from activity import forms as activity_forms

from product.models import Rep, Sale, Payment
#from activity.models import Call, Competition, Contact, MarketNeed, Conclusion
from activity import models as activity_models


@method_decorator(login_required, name='dispatch')
class BaseActivityListView(ListView):
    model = None
    order_by = ''

    def get_queryset(self):
        try:
            rep = Rep.objects.get(user=self.request.user)
        except Rep.DoesNotExist:
            qset = self.model.objects.order_by(self.order_by)
        else:
            qset = self.model.objects.filter(rep=rep).order_by(self.order_by)
        return qset


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
    model = activity_models.Call
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
    calls = activity_models.Call.objects.filter(
        rep=rep).order_by('-call_date')
    return render(request, 'activity/calls_list.html', {'calls': calls})


class CompetitionView(BaseActivityCreateView):
    template_name = 'activity/competition.html'
    form_class = activity_forms.CompetitionForm
    success_url = '/activity/competition/'
    success_msg = 'Successfully added competitor activity'


@login_required
def competition_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    activities = activity_models.Competition.objects.filter(
        rep=rep).order_by('-recorded_date')
    return render(request, 'activity/competition_list.html',
                  {'acts': activities})


class ContactView(BaseActivityCreateView):
    template_name = 'activity/contact.html'
    form_class = activity_forms.ContactForm
    success_url = '/activity/contact/'
    success_msg = 'Successfully added contact'


@login_required
def contact_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    contacts = activity_models.Contact.objects.filter(
        rep=rep).order_by('-added_date')
    return render(request, 'activity/contact_list.html',
                  {'contacts': contacts})


class MarketView(BaseActivityCreateView):
    template_name = 'activity/market.html'
    form_class = activity_forms.MarketForm
    success_url = '/activity/market/'
    success_msg = 'Successfully added market need'


@login_required
def market_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    needs = activity_models.MarketNeed.objects.filter(
        rep=rep).order_by('-recorded_date')
    return render(request, 'activity/market_list.html', {'needs': needs})


class ConclusionView(BaseActivityCreateView):
    template_name = 'activity/conclusion.html'
    form_class = activity_forms.ConclusionForm
    success_url = '/activity/conclusion/'
    success_msg = 'Successfully added conclusion'


@login_required
def conclusion_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    conclusions = activity_models.Conclusion.objects.filter(
        rep=rep).order_by('-recorded_date')
    return render(request, 'activity/conclusion_list.html',
                  {'conclusions': conclusions})


class ItineraryView(BaseActivityCreateView):
    template_name = 'activity/itinerary.html'
    form_class = activity_forms.ItineraryForm
    success_url = '/activity/itinerary/'
    success_msg = 'Successfully added itinerary'


class ItineraryListView(BaseActivityListView):
    model = activity_models.Itinerary
    order_by = '-recorded_date'


class SummaryView(BaseActivityCreateView):
    template_name = 'activity/summary.html'
    form_class = activity_forms.SummaryForm
    success_url = '/activity/summary/'
    success_msg = 'Successfully added summary'

    def form_valid(self, form):
        rep = Rep.objects.get(user=self.request.user)
        obj = form.save(commit=False)
        obj.rep = rep
        total_sales = Sale.objects.filter(invoice__rep=rep).aggregate(
            Sum('amount'))['amount__sum'] or 0
        total_payment = Payment.objects.filter(rep=rep).aggregate(
            Sum('amount'))['amount__sum'] or 0
        obj.outstanding = total_sales - total_payment
        obj.save()
        messages.success(self.request, self.success_msg)
        return super(BaseActivityCreateView, self).form_valid(form)


class SummaryListView(BaseActivityListView):
    model = activity_models.Summary
    order_by = '-start_date'


@login_required
def summary_detail(request, summary_id):
    summary = get_object_or_404(activity_models.Summary, id=summary_id)
    return render(request, 'activity/summary_detail.html',
                  {'summary': summary})
