from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum


class Product(models.Model):
    name = models.CharField(max_length=200)
    rate = models.IntegerField()

    def __unicode__(self):
        return self.name

    @property
    def quantity(self):
        return self.product_sales.aggregate(
            Sum('quantity'))['quantity__sum'] or 0

    @property
    def amount(self):
        return self.product_sales.aggregate(
            Sum('amount'))['amount__sum'] or 0


class Rep(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class Customer(models.Model):
    HOSPITAL = 0
    INSTITUTION = 1
    PHARMACY = 2
    WHOLESELLER = 3
    HEALTH_PERSONNEL = 4
    CUSTOMER_TYPE = (
        (0, 'Hospital'),
        (1, 'Institution'),
        (2, 'Pharmacy'),
        (3, 'Wholeseller'),
        (4, 'Health Personnel'))
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    contact_person = models.CharField(max_length=200, blank=True)
    phone1 = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True, null=True)
    customer_type = models.PositiveIntegerField(choices=CUSTOMER_TYPE)

    def __unicode__(self):
        return self.name

    @property
    def balance(self):
        sales = self.customer_sales.aggregate(
            Sum('amount'))['amount__sum'] or 0
        paymt = self.customer_payments.aggregate(
            Sum('amount'))['amount__sum'] or 0
        return sales - paymt


class Sale(models.Model):
    ACTUAL_SALES = 0
    SOR = 1
    SAMPLES = 2
    SALES_TYPES = ((0, 'Actual Sales'), (1, 'SOR'), (2, 'Samples'))
    rep = models.ForeignKey(Rep, related_name='rep_sales')
    customer = models.ForeignKey(Customer, related_name='customer_sales')
    product = models.ForeignKey(Product, related_name='product_sales')
    quantity = models.PositiveIntegerField()
    amount = models.IntegerField()
    invoice_no = models.CharField(max_length=200, blank=True)
    invoice_date = models.DateField(blank=True, null=True)
    sales_date = models.DateField()
    sales_type = models.PositiveIntegerField(choices=SALES_TYPES)
    recorded_date = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return unicode(self.customer)


class Payment(models.Model):
    EPAYMENT = 0
    CHEQUE = 1
    TELLER = 2
    MODE_OF_PAYMENT = ((0, 'E-Payment'), (1, 'Cheque'), (2, 'Teller'))

    rep = models.ForeignKey(Rep, related_name='rep_payments')
    customer = models.ForeignKey(Customer, related_name='customer_payments')
    amount = models.PositiveIntegerField()
    receipt_no = models.CharField(max_length=50, blank=True)
    payment_date = models.DateField()
    receipt_date = models.DateField()
    recorded_date = models.DateTimeField(default=datetime.now)
    balance = models.IntegerField()
    mode_of_payment = models.PositiveIntegerField(choices=MODE_OF_PAYMENT)
    teller_number = models.CharField(max_length=50, blank=True)
    teller_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.customer)
