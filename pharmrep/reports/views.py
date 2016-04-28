from django.shortcuts import render
from django.db.models.aggregates import Sum

from product.models import Customer, Product, Payment


def balance(request):
    customers = Customer.objects.annotate(
        Sum('customer_sales__amount'), Sum('customer_payments__amount'))
    clist = []
    for customer in customers:
        sale = customer.customer_sales__amount__sum or 0
        payment = customer.customer_payments__amount__sum or 0
        clist.append({'name': customer.name, 'balance': sale - payment})
    return render(request, 'reports/balance.html', {'customers': clist})


def performance(request):
    products = Product.objects.annotate(
        Sum('product_sales__quantity'), Sum('product_sales__amount'))
    return render(request, 'reports/performance.html', {'products': products})


def collection(request):
    collections = Payment.objects.all()
    return render(
        request, 'reports/collection.html', {'collections': collections})
