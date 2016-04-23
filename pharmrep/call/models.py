from __future__ import unicode_literals
from datetime import datetime

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
