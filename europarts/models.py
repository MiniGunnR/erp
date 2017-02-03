from django.db import models
from utils.models import Timestamped


class ProductList(Timestamped):
    ref_no = models.CharField(max_length=20, unique=True)
    original_price_available = models.BooleanField(default=False)

    def __str__(self):
        return self.ref_no


class Product(Timestamped):
    product_list = models.ForeignKey(ProductList)
    description = models.CharField(max_length=255)
    part_no = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)

    quantity = models.SmallIntegerField()
    unit = models.CharField(max_length=20, default='piece(s)')

    original_price = models.IntegerField(blank=True, null=True)

    public_price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{list} - {product}".format(list=self.product_list.ref_no, product=self.part_no)
