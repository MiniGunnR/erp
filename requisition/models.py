from core.models import Department
from django.db import models
from django.urls import reverse
from utils.models import Timestamped
from django.contrib.auth.models import User


class Vendor(Timestamped):
    name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Requisition(Timestamped):
    created_by = models.ForeignKey(User, related_name='created_requisitions')
    modified_by = models.ForeignKey(User, related_name='modified_requisitions')

    # issue_date = models.DateField(auto_now_add=True)

    department = models.ForeignKey(Department)

    vendor = models.ForeignKey(Vendor, blank=True, null=True)

    total = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return "Requisition {0}".format(str(self.id))

    def view_requisition(self):
        return reverse("requisition:requisition-detail-view", args=[str(self.id)])

    def view_work_order(self):
        pass


class Item(Timestamped):
    requisition = models.ForeignKey(Requisition)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    amount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.price
        super(Item, self).save(*args, **kwargs)


class PurchaseOrder(Timestamped):
    reference_no = models.CharField(max_length=50)
    requisition = models.OneToOneField(Requisition)

    def __str__(self):
        return self.reference_no
