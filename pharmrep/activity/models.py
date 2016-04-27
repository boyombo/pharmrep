from __future__ import unicode_literals
from datetime import datetime, date

from django.db import models
from product.models import Customer, Rep


class Call(models.Model):
    GOVT = 0
    PRIVATE = 1
    TRADE = 2
    CALL_TYPES = ((0, 'Government'), (1, 'Private'), (2, 'Trade Calls'))

    rep = models.ForeignKey(Rep)
    customer = models.ForeignKey(Customer, blank=True, null=True)
    contact = models.CharField(max_length=200)
    position = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    products_detailed = models.TextField(blank=True)
    order_value = models.IntegerField(default=0)
    remarks = models.TextField(blank=True)
    call_type = models.PositiveIntegerField(choices=CALL_TYPES)
    call_date = models.DateField()
    recorded_date = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.contact


class Competition(models.Model):
    rep = models.ForeignKey(Rep)
    activity = models.TextField()
    recorded_date = models.DateField(default=date.today)

    def __unicode__(self):
        return unicode(self.rep)


class Contact(models.Model):
    rep = models.ForeignKey(Rep)
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    added_date = models.DateField(default=datetime.now)

    def __unicode__(self):
        return self.name


class MarketNeed(models.Model):
    rep = models.ForeignKey(Rep)
    text = models.TextField(blank=True)
    recorded_date = models.DateField(default=date.today)

    def __unicode__(self):
        return self.text


class Conclusion(models.Model):
    rep = models.ForeignKey(Rep)
    text = models.TextField(blank=True)
    recorded_date = models.DateField(default=date.today)

    def __unicode__(self):
        return self.text
