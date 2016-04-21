from django.shortcuts import render

from product.forms import SaleForm


def sale(request):
    form = SaleForm()
    return render(request, 'product/sale.html', {'form': form})
