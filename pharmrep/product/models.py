from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=200)
    rate = models.IntegerField()

    def __unicode__(self):
        return self.name


class Rep(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone1 = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return self.name


class Sale(models.Model):
    rep = models.ForeignKey(Rep, related_name='rep_sales')
    customer = models.ForeignKey(Customer, related_name='customer_sales')
    product = models.ForeignKey(Product, related_name='product_sales')
    quantity = models.PositiveIntegerField()
    sales_date = models.DateField()
    recorded_date = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return unicode(self.customer)


class Payment(models.Model):
    rep = models.ForeignKey(Rep, related_name='rep_payments')
    customer = models.ForeignKey(Customer, related_name='customer_payments')
    amount = models.PositiveIntegerField()
    receipt_no = models.CharField(max_length=50, blank=True)
    payment_date = models.DateField()
    recorded_date = models.DateTimeField(default=datetime.now)
    balance = models.IntegerField()

    def __unicode__(self):
        return unicode(self.customer)
