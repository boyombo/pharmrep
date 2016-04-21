from django.shortcuts import render

from product.forms import SaleForm, PaymentForm


def sale(request):
    form = SaleForm()
    return render(request, 'product/sale.html', {'form': form})


def payment(request):
    form = PaymentForm()
    return render(request, 'product/payment.html', {'form': form})
