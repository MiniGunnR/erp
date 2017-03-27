import uuid

from django.db import models
from utils.models import Timestamped
from django.contrib.auth.models import User


class Brand(Timestamped):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AutoType(Timestamped):
    brand = models.ForeignKey(Brand)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AutoPart(Timestamped):
    brand = models.ForeignKey(Brand)
    auto_type = models.ForeignKey(AutoType)
    part_no = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return "{brand} {auto_type} [{part_no}]".format(brand=self.brand, auto_type=self.auto_type, part_no=self.part_no)

    class Meta:
        unique_together = ('brand', 'part_no')


class List(Timestamped):
    ref_no = models.CharField(max_length=30, unique=True)

    cost_price_quoted = models.BooleanField(default=False)
    selling_price_quoted = models.BooleanField(default=False)

    def __str__(self):
        return self.ref_no

    class Meta:
        permissions = (
            ("can_add_product_list", "Can add product list"),
        )
        ordering = ['-created']


class Product(Timestamped):
    product_list = models.ForeignKey(List)
    auto_part = models.ForeignKey(AutoPart)

    quantity = models.SmallIntegerField()
    unit = models.CharField(max_length=20, default='pcs')

    cost_price = models.IntegerField(blank=True, null=True)

    selling_price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{list} - {product}".format(list=self.product_list.ref_no, product=self.auto_part)

    class Meta:
        permissions = (
            ("can_view_cost_price", "Can view cost price"),
        )
        get_latest_by = 'created'


class Quotation(Timestamped):
    ref_no = models.CharField(max_length=50)
    recipient = models.CharField(max_length=255, blank=True, null=True)
    recipient_address = models.CharField(max_length=255, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.ref_no

    class Meta:
        ordering = ['-created']


class QuotationProduct(Timestamped):
    quotation = models.ForeignKey(Quotation)
    auto_part = models.ForeignKey(AutoPart)

    price = models.IntegerField()
    quantity = models.SmallIntegerField()
    unit = models.CharField(max_length=20, default='pcs')
    total = models.IntegerField()

    def __str__(self):
        return "{quotation} - {product}".format(quotation=self.quotation.ref_no, product=self.auto_part)


class QuotationCode(Timestamped):
    quotation = models.ForeignKey(Quotation)
    user = models.ForeignKey(User)
    code = models.CharField(max_length=6, default=str(uuid.uuid4().int)[:6])
    allowed = models.BooleanField(default=False)

    work_order_printed = models.BooleanField(default=False)

    def __str__(self):
        return "{quotation} - {user} - {code}".format(quotation=self.quotation.ref_no, user=self.user, code=self.code)

    class Meta:
        unique_together = ('quotation', 'user')
