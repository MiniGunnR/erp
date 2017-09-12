from django.db import models
from utils.models import Timestamped
from django.shortcuts import reverse


class Inventory(Timestamped):
    name = models.CharField(max_length=100)
    uid = models.CharField(max_length=50, unique=True)
    lc = models.CharField(max_length=20, blank=True)
    spinning_mills = models.CharField(max_length=20, blank=True)
    composition = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.uid

    def get_absolute_url(self):
        return reverse('inv:inventory_detailview', args=[self.pk])

    def increase_quantity(self, quantity):
        self.quantity += quantity
        self.save()

    def decrease_quantity(self, quantity):
        self.quantity -= quantity
        self.save()

