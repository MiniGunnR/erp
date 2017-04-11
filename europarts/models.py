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


class Inventory(Timestamped):
    part_no = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.part_no

    class Meta:
        verbose_name_plural = 'Inventory'


class Worksheet(Timestamped):
    ref_no = models.CharField(max_length=100)

    quotation_ref = models.CharField(max_length=100, blank=True, null=True)

    cost_price_visible = models.BooleanField(default=True)
    sale_price_visible = models.BooleanField(default=True)
    total_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.ref_no

    class Meta:
        ordering = ['-created']


class WorksheetRow(Timestamped):
    worksheet = models.ForeignKey(Worksheet)
    part_no = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit_margin = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.part_no


class Quotation(Timestamped):
    ref_no = models.CharField(max_length=100)
    worksheet = models.ForeignKey(Worksheet)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    recipient = models.CharField(max_length=100, default='')
    recipient_address = models.CharField(max_length=255, default='')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.ref_no


class QuotationRow(Timestamped):
    quotation = models.ForeignKey(Quotation)
    part_no = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.part_no


class Invoice(Timestamped):
    ref_no = models.CharField(max_length=100)
    quotation = models.ForeignKey(Quotation)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_after_tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    recipient = models.CharField(max_length=100, default='')
    recipient_address = models.CharField(max_length=255, default='')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.ref_no


class InvoiceRow(Timestamped):
    invoice = models.ForeignKey(Invoice)
    part_no = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.part_no


class Challan(Timestamped):
    ref_no = models.CharField(max_length=100)
    invoice = models.ForeignKey(Invoice)
    recipient = models.CharField(max_length=100, default='')
    recipient_address = models.CharField(max_length=255, default='')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.ref_no


class ChallanRow(Timestamped):
    challan = models.ForeignKey(Challan)
    part_no = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return self.part_no