from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from product.forms import SaleForm, PaymentForm


@login_required
def sale(request):
    form = SaleForm()
    return render(request, 'product/sale.html', {'form': form})


@login_required
def payment(request):
    form = PaymentForm()
    return render(request, 'product/payment.html', {'form': form})
