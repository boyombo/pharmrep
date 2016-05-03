from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.aggregates import Sum

from activity import forms as activity_forms
from core.views import BaseActivityCreateView, BaseActivityListView

from product.models import Sale, Payment
#from activity.models import Call, Competition, Contact, MarketNeed, Conclusion
from activity import models as activity_models


#@method_decorator(login_required, name='dispatch')
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


class CallListView(BaseActivityListView):
    model = activity_models.Call
    order_by = '-call_date'


class CompetitionView(BaseActivityCreateView):
    template_name = 'activity/competition.html'
    form_class = activity_forms.CompetitionForm
    success_url = '/activity/competition/'
    success_msg = 'Successfully added competitor activity'


class CompetitionListView(BaseActivityListView):
    model = activity_models.Competition


class ContactView(BaseActivityCreateView):
    template_name = 'activity/contact.html'
    form_class = activity_forms.ContactForm
    success_url = '/activity/contact/'
    success_msg = 'Successfully added contact'


class ContactListView(BaseActivityListView):
    model = activity_models.Contact
    order_by = '-added_date'


class MarketView(BaseActivityCreateView):
    template_name = 'activity/market.html'
    form_class = activity_forms.MarketForm
    success_url = '/activity/market/'
    success_msg = 'Successfully added market need'


class MarketListView(BaseActivityListView):
    model = activity_models.MarketNeed


class ConclusionView(BaseActivityCreateView):
    template_name = 'activity/conclusion.html'
    form_class = activity_forms.ConclusionForm
    success_url = '/activity/conclusion/'
    success_msg = 'Successfully added conclusion'


class ConclusionListView(BaseActivityListView):
    model = activity_models.Conclusion


class ItineraryView(BaseActivityCreateView):
    template_name = 'activity/itinerary.html'
    form_class = activity_forms.ItineraryForm
    success_url = '/activity/itinerary/'
    success_msg = 'Successfully added itinerary'


class ItineraryListView(BaseActivityListView):
    model = activity_models.Itinerary


class SummaryView(BaseActivityCreateView):
    template_name = 'activity/summary.html'
    form_class = activity_forms.SummaryForm
    success_url = '/activity/summary/'
    success_msg = 'Successfully added summary'

    def form_valid(self, form):
        #rep = Rep.objects.get(user=self.request.user)
        rep = self.request.user.rep
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
