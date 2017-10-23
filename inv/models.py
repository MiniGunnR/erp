from django.db import models
from utils.models import Timestamped
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models import Sum


class Inventory(Timestamped):
    name = models.CharField(max_length=100)
    uid = models.CharField(max_length=50, unique=True)
    lc = models.CharField(max_length=20, blank=True)
    spinning_mills = models.CharField(max_length=20, blank=True)
    composition = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveSmallIntegerField(default=0)

    created_by = models.ForeignKey(User, related_name='inventory_created', blank=True, null=True)
    modified_by = models.ForeignKey(User, related_name='inventory_modified', blank=True, null=True)

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


class LetterOfCredit(Timestamped):
    """ This model saves LC information
        to be used with yarns received model.
    """
    date = models.DateField()
    number = models.CharField(max_length=20)
    spinning_mill = models.CharField(max_length=50)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return reverse('inv:lc_updateview', args=[str(self.id)])


class LCItem(Timestamped):
    """ Stores items in the LC.
    """
    lc = models.ForeignKey(LetterOfCredit)
    count = models.CharField(max_length=20)
    item = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "{lc} Count: {count} Comp: {item}".format(lc=self.lc, count=self.count, item=self.item)


class YarnReceived(Timestamped):
    """ Stores yarn received in relation to LCs.
    """
    date = models.DateField()
    lc_item = models.ForeignKey(LCItem)
    challan_no = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    barcode = models.CharField(max_length=50, default='000000000000')  # make unique

    class Meta:
        ordering = ['lc_item']

    def __str__(self):
        return "{lc_item}".format(lc_item=self.lc_item)

    def rcvd(self):
        objs = YarnReceived.objects.filter(lc_item=self.lc_item)
        received = objs.aggregate(Sum('quantity'))['quantity__sum']
        if received is None:
            return 0
        return received

    def balance(self):
        return self.lc_item.quantity - self.rcvd()

    def decrease_quantity(self, quantity):
        self.quantity -= quantity
        self.save()

    def save(self, *args, **kwargs):
        if self.balance() >= self.quantity:
            super(YarnReceived, self).save(*args, **kwargs)
        else:
            raise ValueError("Quantity is greater than available.")


class YarnDelivery(Timestamped):
    """ Stores yarn delivered in relation to yarn received.
    """
    yr = models.ForeignKey(YarnReceived, verbose_name="Yarn Received")
    date = models.DateField()
    challan_no = models.CharField(max_length=20)
    colour = models.CharField(max_length=20)
    style_no = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    barcode = models.CharField(max_length=50, default='000000000000')  # make unique

    def __str__(self):
        return "{colour} {style_no}".format(colour=self.colour, style_no=self.style_no)

    def get_absolute_url(self):
        return reverse('inv:yd_updateview', args=[str(self.id)])

    def rcvd(self):
        objs = YarnDelivery.objects.filter(yr=self.yr)
        received = objs.aggregate(Sum('quantity'))['quantity__sum']
        if received is None:
            return 0
        return received

    def balance(self):
        return self.yr.quantity - self.rcvd()

    def decrease_quantity(self, quantity):
        self.quantity -= quantity
        self.save()

    def save(self, *args, **kwargs):
        if self.balance() >= self.quantity:
            super(YarnDelivery, self).save(*args, **kwargs)
        else:
            raise ValueError("Quantity is greater than available.")


class FabricDelivery(Timestamped):
    yd = models.ForeignKey(YarnDelivery, verbose_name="Yarn Delivered")
    date = models.DateField()
    challan_no = models.CharField(max_length=20)
    fabric_type = models.CharField(max_length=20)
    colour = models.CharField(max_length=20)
    dy_name = models.CharField(max_length=40)
    barcode = models.CharField(max_length=50, default='000000000000')  # make unique

    def __str__(self):
        return "{fabric_type} {colour}".format(fabric_type=self.fabric_type, colour=self.colour)

    def get_absolute_url(self):
        return reverse('inv:fd_updateview', args=[str(self.id)])
