from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum


class PriceTemplate(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    rate = models.IntegerField('Default price of product')
    template = models.ManyToManyField(
        PriceTemplate,
        through='ProductPriceTemplate',
        through_fields=('product', 'template'))

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


class ProductPriceTemplate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    template = models.ForeignKey(PriceTemplate, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __unicode__(self):
        return "{0} - {1}".format(self.product, self.template)


class BatchSize(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name


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
    price_template = models.ForeignKey(PriceTemplate, null=True, blank=True)

    def __unicode__(self):
        return self.name

    @property
    def balance(self):
        sales = Sale.objects.filter(invoice__customer=self).aggregate(
            Sum('amount'))['amount__sum'] or 0
        #sales = self.customer_sales.aggregate(
        #    Sum('amount'))['amount__sum'] or 0
        paymt = self.customer_payments.aggregate(
            Sum('amount'))['amount__sum'] or 0
        return sales - paymt


class Invoice(models.Model):
    ACTUAL_SALES = 0
    SOR = 1
    SAMPLES = 2
    INVOICE_TYPES = ((0, 'Actual Sales'), (1, 'SOR'), (2, 'Samples'))
    rep = models.ForeignKey(Rep, related_name='rep_invoices')
    customer = models.ForeignKey(Customer, related_name='customer_invoices')
    invoice_no = models.CharField(max_length=200, blank=True)
    invoice_date = models.DateField(blank=True, null=True)
    sales_type = models.PositiveIntegerField(choices=INVOICE_TYPES)
    recorded_date = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return unicode(self.invoice_no)

    @property
    def amount(self):
        return sum([sale.amount for sale in self.invoice_sales.all()])


class Sale(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name='invoice_sales', null=True)
    product = models.ForeignKey(Product, related_name='product_sales')
    batch_size = models.ForeignKey(BatchSize, null=True)
    quantity = models.PositiveIntegerField()
    amount = models.IntegerField()
    recorded_date = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return unicode(self.customer)

    @property
    def rate(self):
        templ = self.invoice.customer.price_template
        if not templ:
            price = self.product.rate
        else:
            try:
                prod_price_templ = ProductPriceTemplate.objects.get(
                    product=self.product, template=templ)
            except ProductPriceTemplate.DoesNotExist:
                price = self.product.rate
            else:
                price = prod_price_templ.price
        return price


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
    bank_of_payment = models.CharField(max_length=200, blank=True)
    mode_of_payment = models.PositiveIntegerField(choices=MODE_OF_PAYMENT)
    teller_number = models.CharField(max_length=50, blank=True)
    teller_date = models.DateField(blank=True, null=True)
    cheque_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.customer)
