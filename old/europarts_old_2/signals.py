from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import QuotationProduct, Quotation


def add_to_total(instance, created, **kwargs):
    pass
