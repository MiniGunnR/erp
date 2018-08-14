from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job


@receiver(post_save, sender=Job)
def add_job_no_serial(instance, created, **kwargs):
    if created:
        instance.job_no = instance.job_no + "-" + str(instance.pk)
        instance.save()
