from core.models import Department
from django.db import models
from django.urls import reverse
from utils.models import Timestamped
from django.contrib.auth.models import User

from core.models import Company


class Vendor(Timestamped):
    name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Requisition(Timestamped):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, related_name='created_requisitions', on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, related_name='modified_requisitions', on_delete=models.CASCADE)

    issue_date = models.DateField(blank=True, null=True)

    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.CASCADE)

    total = models.FloatField(blank=True, null=True, default=0)

    read_only = models.BooleanField(default=False)

    def __str__(self):
        return "Requisition {0}".format(str(self.id))

    def view_requisition(self):
        return reverse("requisition:requisition-pdf-view", args=[str(self.id)])

    def view_work_order(self):
        self.read_only = True
        self.save()
        return reverse("requisition:purchase-order", args=[str(self.id)])


class Item(Timestamped):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
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
    requisition = models.OneToOneField(Requisition, on_delete=models.CASCADE)

    def __str__(self):
        return self.reference_no


class QuotationRequest(Timestamped):
    vendor = models.ForeignKey(Vendor)
    email = models.EmailField()

    def __str__(self):
        return "DAL-IT_{}".format(self.pk)

class QuotationRequestItem(Timestamped):
    quotationrequest = models.ForeignKey(QuotationRequest)
    name = models.CharField(max_length=200)
    quantity = models.SmallIntegerField()

    def __str__(self):
        return "{qr} - {name}".format(qr=self.quotationrequest, name=self.name)
