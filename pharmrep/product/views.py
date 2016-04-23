from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Sum
from django.contrib import messages

from product.forms import SaleForm, PaymentForm
from product.models import Rep, Sale, Payment


@login_required
def sale(request):
    try:
        rep = Rep.objects.get(user=request.user)
    except Rep.DoesNotExist:
        messages.error(request, 'You need to be a rep to make sales')
        return redirect('/accounts/login/')
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.rep = rep
            obj.amount = obj.quantity * obj.product.rate
            obj.save()
            return redirect('sales_list')
    else:
        form = SaleForm()
    return render(request, 'product/sale.html', {'form': form})


@login_required
def sales_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    sales = Sale.objects.filter(rep=rep)
    return render(request, 'product/sales_list.html', {'sales': sales})


@login_required
def payment(request):
    try:
        rep = Rep.objects.get(user=request.user)
    except Rep.DoesNotExist:
        messages.error(request, 'You need to be a rep to make collections')
        return redirect('/accounts/login/')
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amt = form.cleaned_data['amount']
            obj = form.save(commit=False)
            obj.rep = rep
            total_sales = Sale.objects.filter(
                customer=obj.customer, rep=rep).aggregate(
                Sum('amount'))['amount__sum'] or 0
            total_payment = Payment.objects.filter(
                customer=obj.customer, rep=rep).aggregate(
                Sum('amount'))['amount__sum'] or 0
            obj.balance = total_sales - total_payment - amt
            obj.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'product/payment.html', {'form': form})


@login_required
def payment_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    payments = Payment.objects.filter(rep=rep)
    return render(request, 'product/payment_list.html', {'payments': payments})
