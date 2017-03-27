from django.db import models

from utils.models import Timestamped


class Brand(Timestamped):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Type(Timestamped):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Part(Timestamped):
    brand = models.ForeignKey(Brand)
    type = models.ForeignKey(Type)
    part_no = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.part_no


class Worksheet(Timestamped):
    ref_no = models.CharField(max_length=100)

    def __str__(self):
        return self.ref_no


class WorksheetRow(Timestamped):
    worksheet = models.ForeignKey(Worksheet)
    part_no = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.part_no
