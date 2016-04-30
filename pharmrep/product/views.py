from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Sum
from django.contrib import messages
#from django.views.generic.edit import CreateView

from product.forms import SaleForm, PaymentForm, InvoiceForm
from product.models import Rep, Sale, Payment, Invoice


@login_required
def invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.user, request.POST)
        if form.is_valid():
            rep = Rep.objects.get(user=request.user)
            invoice = form.save(commit=False)
            invoice.rep = rep
            invoice.save()
            messages.success(request, 'Successfully added invoice')
            return redirect('product_sale', invoice.id)
    else:
        form = InvoiceForm(request.user)
    return render(request, 'product/invoice.html', {'form': form})


@login_required
def sale(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == 'POST':
        form = SaleForm(request.POST)
        #import pdb;pdb.set_trace()
        if form.is_valid():
            sale = form.save(commit=False)
            sale.invoice = invoice
            sale.amount = sale.quantity * sale.product.rate *\
                sale.batch_size.quantity
            sale.save()
            #rep = Rep.objects.get(user=request.user)
            #obj = form.save(commit=False)
            #obj.rep = rep
            #obj.amount = obj.quantity * obj.product.rate
            #obj.save()
            messages.success(
                request, 'Successfully added sale to invoice {}'.format(
                    invoice.invoice_no))
            return redirect('product_sale', invoice.id)
    else:
        form = SaleForm()
    return render(request, 'product/sale.html', {
        'form': form,
        'invoice': invoice
    })


@login_required
def invoice_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    invoices = Invoice.objects.filter(rep=rep).order_by('-invoice_date')
    #sales = Sale.objects.filter(rep=rep).order_by('-sales_date')
    return render(request, 'product/invoice_list.html', {'invoices': invoices})


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
            messages.success(request, 'Successfully added collection')
            #return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'product/payment.html', {'form': form})


@login_required
def payment_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    payments = Payment.objects.filter(rep=rep)
    return render(request, 'product/payment_list.html', {'payments': payments})
