from django.db import models
from django.utils import timezone


class Rate(models.Model):
    exchange_rate = models.CharField(max_length=300, blank=True, null=True)
    bid_price = models.CharField(max_length=300, blank=True, null=True)
    ask_price = models.CharField(max_length=300, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now(), blank=True)

    def __str__(self):
        return self.exchange_rate


class Currency(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    rate = models.ManyToManyField(Rate)

    def __str__(self):
        return self.name
