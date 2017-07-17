from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings

from .models import EmployeeLeave, Leave, Default


@receiver(post_save, sender=EmployeeLeave)
def save_employee_leave_with_default(instance, created, **kwargs):
    if created:
        sl_obj = Default.objects.get(attribute='Sick Leave')
        instance.sick_leave = int(sl_obj.value)

        cl_obj = Default.objects.get(attribute='Casual Leave')
        instance.casual_leave = int(cl_obj.value)


@receiver(post_save, sender=Leave)
def subtract_leave_day(instance, created, **kwargs):
    if created:
        try:
            emp_lv_obj = EmployeeLeave.objects.get(emp_id=instance.emp_id)
        except EmployeeLeave.DoesNotExist:
            emp_lv_obj = EmployeeLeave.objects.create(emp_id=instance.emp_id, sick_leave=0, casual_leave=0)
        if instance.type == 'SL':
            emp_lv_obj.sick_leave -= 1
        elif instance.type == 'CL':
            emp_lv_obj.casual_leave -= 1
        emp_lv_obj.save()


@receiver(post_delete, sender=Leave)
def add_back_leave_day(instance, **kwargs):
    try:
        emp_lv_obj = EmployeeLeave.objects.get(emp_id=instance.emp_id)
    except EmployeeLeave.DoesNotExist:
        pass
    else:
        if instance.type == 'SL':
            emp_lv_obj.sick_leave += 1
        elif instance.type == 'CL':
            emp_lv_obj.casual_leave += 1
        emp_lv_obj.save()
