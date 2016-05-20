from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#from product.models import Rep
from core.forms import SearchForm


@method_decorator(login_required, name='dispatch')
class BaseActivityListView(ListView):
    model = None
    order_by = '-recorded_date'
    order_by_extra = None

    def get_context_data(self, **kwargs):
        context = super(BaseActivityListView, self).get_context_data(**kwargs)
        form = SearchForm(self.request.user.rep, self.request.GET)
        context.update({'form': form})
        return context

    def get_queryset(self):
        params = {}
        #import pdb;pdb.set_trace()
        form = SearchForm(self.request.user.rep, self.request.GET)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            rep = form.cleaned_data['rep']

            date_fld = self.order_by
            if date_fld[0] == '-':
                date_fld = date_fld[1:]

            #params.update({'{}__range'.format(date_fld): (start, end)})
            if start:
                params.update({'{}__gte'.format(date_fld): start})
            if end:
                params.update({'{}__lte'.format(date_fld): end})
            if rep:
                params.update({'rep': rep})
        else:
            #subordinates = [r for r in Rep.objects.filter(supervisor=rep)]
            #all_reps = [rep] + subordinates
            #params.update({'rep__in': all_reps})
            params.update({'rep': self.request.user.rep})
        ordering = [self.order_by]
        if self.order_by_extra:
            ordering.append(self.order_by_extra)
        return self.model.objects.filter(**params).order_by(*ordering)


@method_decorator(login_required, name='dispatch')
class BaseActivityCreateView(CreateView):
    model = None
    success_msg = None
    success_url = None

    def get_form_kwargs(self):
        kwargs = super(BaseActivityCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    #def get_success_url(self):
    #    return self.success_url

    def form_valid(self, form):
        #import pdb;pdb.set_trace()
        self.object = form.save(commit=False)
        self.object.rep = self.request.user.rep
        #obj.rep = Rep.objects.get(user=self.request.user)
        self.object.save()
        messages.success(self.request, self.success_msg)
        return super(BaseActivityCreateView, self).form_valid(form)
