from __future__ import unicode_literals
from datetime import datetime, date

from django.db import models
from django.db.models.aggregates import Sum
from product.models import Customer, Rep, Sale, Payment, Product


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
    product = models.ForeignKey(Product, null=True, blank=True)
    competing_company = models.CharField(max_length=200, blank=True)
    competing_product = models.CharField(max_length=200, blank=True)
    activity = models.TextField(blank=True)
    expected_effect = models.TextField(blank=True)
    suggestion = models.TextField(blank=True)
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


class Itinerary(models.Model):
    rep = models.ForeignKey(Rep)
    recorded_date = models.DateField(default=date.today)
    places = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Itinerary'

    def __unicode__(self):
        return self.places


class Summary(models.Model):
    rep = models.ForeignKey(Rep)
    start_date = models.DateField()
    end_date = models.DateField()
    outstanding = models.IntegerField(default=0)
    report = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Summaries'

    def __unicode__(self):
        return unicode(self.rep)

    @property
    def sales(self):
        return Sale.objects.filter(
            invoice__rep=self.rep,
            invoice__invoice_date__range=(self.start_date, self.end_date)
            ).aggregate(Sum('amount'))['amount__sum'] or 0

    @property
    def collections(self):
        return Payment.objects.filter(
            rep=self.rep,
            payment_date__range=(self.start_date, self.end_date)).aggregate(
            Sum('amount'))['amount__sum'] or 0

    @property
    def calls(self):
        return Call.objects.filter(
            rep=self.rep,
            call_date__range=(self.start_date, self.end_date)).count()

    @property
    def contacts(self):
        return Contact.objects.filter(
            rep=self.rep,
            added_date__range=(self.start_date, self.end_date)).count()
