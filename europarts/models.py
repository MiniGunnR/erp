from django.db import models

from utils.models import Timestamped


class Client(Timestamped):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Brand(Timestamped):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


TYPE_CHOICES = (
    ('Vehicle', 'Vehicle'),
    ('Marine', 'Marine'),
)


class Type(Timestamped):
    name = models.CharField(max_length=50, unique=True, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name


class Part(Timestamped):
    # for marine
    engine_no = models.CharField(max_length=50, blank=True, null=True)
    ship_name = models.CharField(max_length=100, blank=True, null=True)

    # for vehicle
    serial_no = models.CharField(max_length=50, blank=True, null=True)
    chassis_no = models.CharField(max_length=50, blank=True, null=True)

    part_no = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.part_no


class Inventory(Timestamped):
    part_no = models.CharField(max_length=100)
    barcode = models.CharField(max_length=255)
    brand = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True, choices=TYPE_CHOICES)
    description = models.CharField(max_length=255, blank=True, null=True)

    # for marine
    engine_no = models.CharField(max_length=50, blank=True)
    ship_name = models.CharField(max_length=100, blank=True)

    # for vehicle
    serial_no = models.CharField(max_length=50, blank=True)
    chassis_no = models.CharField(max_length=50, blank=True)

    quantity = models.IntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.part_no

    class Meta:
        verbose_name_plural = 'Inventory'


class Worksheet(Timestamped):
    ref_no = models.CharField(max_length=100)

    quotation_ref = models.CharField(max_length=100, blank=True, null=True)
    display_id = models.IntegerField(default=5)

    cost_price_visible = models.BooleanField(default=True)
    sale_price_visible = models.BooleanField(default=True)
    total_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.ref_no

    def save(self, *a, **kw):
        try:
            self.display_id = Worksheet.objects.order_by('created').last().display_id
        except:
            self.display_id = 5
        else:
            self.display_id += 5
        super(Worksheet, self).save(*a, **kw)

    class Meta:
        ordering = ['-created']


class WorksheetRow(Timestamped):
    worksheet = models.ForeignKey(Worksheet)
    part_no = models.CharField(max_length=100, blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(null=True)
    gram_p_s = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    per_pcs_duty_tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    air_freight_cost_p_pcs = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_purchase_price_taka = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_after_tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit_price_in_taka = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    total_price_in_taka = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.part_no


class Quotation(Timestamped):
    ref_no = models.CharField(max_length=100)
    worksheet = models.ForeignKey(Worksheet)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # recipient = models.CharField(max_length=100, default='')
    # recipient_address = models.CharField(max_length=255, default='')
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, blank=True, null=True)

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
    paid = models.BooleanField(default=False)

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

