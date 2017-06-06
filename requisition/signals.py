from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Item
from django.db.models import Sum


@receiver(post_save, sender=Item)
def calculate_total(instance, created, **kwargs):
    total = Item.objects.filter(requisition=instance.requisition).aggregate(Sum('amount'))
    instance.requisition.total = total['amount__sum']
    instance.requisition.save()


@receiver(post_delete, sender=Item)
def decrease_total(instance, **kwargs):
    total = Item.objects.filter(requisition=instance.requisition).aggregate(Sum('amount'))
    instance.requisition.total = total['amount__sum']
    instance.requisition.save()

