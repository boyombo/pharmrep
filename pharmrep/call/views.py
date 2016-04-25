from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.edit import CreateView


from call.forms import GovtCallForm, PrivateCallForm, TradeCallForm
from product.models import Rep
from call.models import Call


@method_decorator(login_required, name='dispatch')
class CallView(CreateView):
    model = Call
    #form_class = CallForm
    #template_name = 'call/call.html'
    #success_url = '/call/call/'

    def get_form_kwargs(self):
        kwargs = super(CallView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return '/call/call/'

    def form_valid(self, form):
        messages.success(self.request, 'Successfully added call')
        return super(CallView, self).form_valid(form)


class GovtCallView(CallView):
    template_name = 'call/govt.html'
    form_class = GovtCallForm

    def get_success_url(self):
        return 'call/govt/'


class PrivateCallView(CallView):
    template_name = 'call/private.html'
    form_class = PrivateCallForm

    def get_success_url(self):
        return 'call/private/'


class TradeCallView(CallView):
    template_name = 'call/trade.html'
    form_class = TradeCallForm

    def get_success_url(self):
        return 'call/trade/'


@login_required
def call_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    calls = Call.objects.filter(rep=rep).order_by('-call_date')
    return render(request, 'call/calls_list.html', {'calls': calls})
