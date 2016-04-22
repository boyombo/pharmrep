from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from product.forms import SaleForm, PaymentForm
from product.models import Rep


@login_required
def sale(request):
    rep = get_object_or_404(Rep, user=request.user)
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.rep = rep
            obj.save()
    else:
        form = SaleForm()
    return render(request, 'product/sale.html', {'form': form})


@login_required
def payment(request):
    form = PaymentForm()
    return render(request, 'product/payment.html', {'form': form})
