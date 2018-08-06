from django.db import models

from utils.models import Timestamped


class Item(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OrderCollection(Timestamped):
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    order_no = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    quantity = models.PositiveSmallIntegerField(default=1)
    unit_price = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.order_no
