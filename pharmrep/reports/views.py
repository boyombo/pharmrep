from django.shortcuts import render
#from django.db.models.aggregates import Sum

from product.models import Customer, Product, Payment, Rep
from core.views import BaseActivityListView


def last_activity(request):
    return render(request, 'reports/last_activity.html',
                  {'reps': Rep.objects.all()})


def balance(request):
    return render(request, 'reports/balance.html',
                  {'customers': Customer.objects.all()})
    #customers = Customer.objects.annotate(
    #    Sum('customer_sales__amount'), Sum('customer_payments__amount'))
    #clist = []
    #for customer in customers:
    #    sale = customer.customer_sales__amount__sum or 0
    #    payment = customer.customer_payments__amount__sum or 0
    #    clist.append({'name': 'name', 'balance': sale - payment})
    #return render(request, 'reports/balance.html', {'customers': clist})


def performance(request):
    #products = Product.objects.annotate(
    #    Sum('product_sales__quantity'), Sum('product_sales__amount'))
    return render(request, 'reports/performance.html',
                  {'products': Product.objects.all()})


class CollectionListView(BaseActivityListView):
    model = Payment
    order_by = '-receipt_date'
    template_name = 'reports/collection.html'


def collection(request):
    collections = Payment.objects.all()
    return render(
        request, 'reports/collection.html', {'collections': collections})
