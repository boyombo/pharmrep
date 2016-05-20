from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.aggregates import Sum
from django.forms.models import modelformset_factory

from activity import forms as activity_forms
from core.views import BaseActivityCreateView, BaseActivityListView

from product.models import Sale, Payment
#from activity.models import Call, Competition, Contact, MarketNeed, Conclusion
from activity import models as activity_models
from core.decorators import last_activity


#@method_decorator(login_required, name='dispatch')
class CallView(BaseActivityCreateView):
    model = activity_models.Call
    success_msg = 'Successfully added call'
    #success_url = '/activity/govt/'
    success_url = '/activity/products/%(id)s'

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super(BaseActivityCreateView, self).form_valid(form)


class GovtCallView(CallView):
    template_name = 'activity/govt.html'
    form_class = activity_forms.GovtCallForm

    #def get_success_url(self):
    #    #import pdb;pdb.set_trace()
    #    return '/activity/products/{id}/'.format(self.object.id)
    #success_url = '/activity/products/%(id)s'
    # success_url = '/activity/govt/'


class PrivateCallView(CallView):
    template_name = 'activity/private.html'
    form_class = activity_forms.PrivateCallForm
    #success_url = '/activity/private/'


class TradeCallView(CallView):
    template_name = 'activity/trade.html'
    form_class = activity_forms.TradeCallForm
    #success_url = '/activity/trade/'


class CallListView(BaseActivityListView):
    model = activity_models.Call
    order_by = '-call_date'


def call_detail(request, call_id):
    call = activity_models.Call.objects.get(id=call_id)
    return render(request, 'activity/call_detail.html', {'call': call})


@login_required
@last_activity
def product_detailed(request, call_id):
    call = activity_models.Call.objects.get(id=call_id)
    detailed = activity_models.ProductDetail.objects.filter(call=call)
    if request.method == 'POST':
        form = activity_forms.ProductDetailedForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.call = call
            obj.save()
            messages.info(request, "Added product detail successfully")
            return redirect('product_detailed', call_id=call_id)
    else:
        form = activity_forms.ProductDetailedForm()
    return render(request, 'activity/products_detailed.html', {
        'form': form, 'call': call, 'detail_list': detailed})


@login_required
@last_activity
def remove_order(request, detail_id):
    detail = activity_models.ProductDetail.objects.get(pk=detail_id)
    call = detail.call
    detail.delete()
    messages.info(request, "Removed product detail successfully")
    return redirect('product_detailed', call_id=call.id)


class CompetitionView(BaseActivityCreateView):
    template_name = 'activity/competition.html'
    form_class = activity_forms.CompetitionForm
    success_url = '/activity/competition/'
    success_msg = 'Successfully added competitor activity'


class CompetitionListView(BaseActivityListView):
    model = activity_models.Competition


def competition_detail(request, entry_id):
    entry = activity_models.Competition.objects.get(id=entry_id)
    return render(request,
                  'activity/competition_detail.html', {'entry': entry})


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


@login_required
@last_activity
def edit_itinerary(request, item_id):
    itinerary = activity_models.Itinerary.objects.get(id=item_id)
    if request.method == 'POST':
        form = activity_forms.ItineraryForm(request.POST, instance=itinerary)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully saved itinerary')
            return redirect('itinerary_list')
    else:
        form = activity_forms.ItineraryForm(instance=itinerary)
    return render(request, 'activity/edit_itinerary.html',
                  {'form': form, 'itinerary': itinerary})


@login_required
@last_activity
def itinerary(request):
    rep = request.user.rep
    ItineraryFormset = modelformset_factory(
        activity_models.Itinerary, fields=('time_slot', 'activity'), extra=10)
    if request.method == 'POST':
        formset = ItineraryFormset(
            request.POST, queryset=activity_models.Itinerary.objects.none())
        date_form = activity_forms.DateForm(request.POST)
        #import pdb;pdb.set_trace()
        if formset.is_valid() and date_form.is_valid():
            dt = date_form.cleaned_data['date']
            instances = formset.save(commit=False)
            for instance in instances:
                try:
                    obj = activity_models.Itinerary.objects.get(
                        rep=rep,
                        recorded_date=dt,
                        time_slot=instance.time_slot)
                except activity_models.Itinerary.DoesNotExist:
                    instance.rep = rep
                    instance.recorded_date = dt
                    instance.save()
                else:
                    obj.time_slot = instance.time_slot
                    obj.activity = instance.activity
                    obj.save()

            messages.success(request, "Successfully entered your itinerary")
            return redirect('itinerary')
    else:
        formset = ItineraryFormset(
            queryset=activity_models.Itinerary.objects.none())
        date_form = activity_forms.DateForm()
    return render(request, 'activity/itinerary.html',
                  {'formset': formset, 'date_form': date_form})


class ItineraryView(BaseActivityCreateView):
    template_name = 'activity/itinerary.html'
    form_class = activity_forms.ItineraryForm
    success_url = '/activity/itinerary/'
    success_msg = 'Successfully added itinerary'


class ItineraryListView(BaseActivityListView):
    model = activity_models.Itinerary
    order_by = 'recorded_date'
    order_by_extra = 'time_slot'


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
