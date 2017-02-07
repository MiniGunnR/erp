from django.db import models
from utils.models import Timestamped


class CarPart(Timestamped):
    part_no = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    brand = models.CharField(max_length=50)

    def __str__(self):
        return "{description} - {part_no}".format(description=self.description, part_no=self.part_no)


class List(Timestamped):
    ref_no = models.CharField(max_length=20, unique=True)

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
    car_part = models.ForeignKey(CarPart)

    quantity = models.SmallIntegerField()
    unit = models.CharField(max_length=20, default='pcs')

    cost_price = models.IntegerField(blank=True, null=True)

    selling_price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{list} - {product}".format(list=self.product_list.ref_no, product=self.car_part)

    class Meta:
        permissions = (
            ("can_view_cost_price", "Can view cost price"),
            ("can_add_cost_price", "Can add cost price"),
            ("can_edit_cost_price", "Can edit cost price"),

            ("can_view_selling_price", "Can view selling price"),
            ("can_add_selling_price", "Can add selling price"),
            ("can_edit_selling_price", "Can edit selling price"),
        )

