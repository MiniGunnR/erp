from django import template

register = template.Library()

from datetime import datetime

from ..models import Attn, Leave, OffDay
from ..views import WEEKLY_OFF


@register.filter(name='fetch_attendance')
def fetch_attendance(date, emp_id):
    try:
        obj = Attn.objects.get(emp_id=emp_id, dt=date, type='N')
    except Attn.DoesNotExist:
        ent = 'ABS'
        if datetime.strptime(date, "%Y-%m-%d").weekday() == WEEKLY_OFF:
            ent = 'OFF'
    else:
        ent = obj.tm.strftime("%H:%M")
    try:
        obj = Attn.objects.get(emp_id=emp_id, dt=date, type='X')
    except Attn.DoesNotExist:
        ext = 'X'
        if datetime.strptime(date, "%Y-%m-%d").weekday() == WEEKLY_OFF:
            ext = ''
    else:
        ext = obj.tm.strftime("%H:%M")

    try:
        obj = OffDay.objects.get(date=date)
    except OffDay.DoesNotExist:
        pass
    else:
        ent = obj.details
        ext = ''

    try:
        obj = Leave.objects.get(emp_id=emp_id, date=date)
    except Leave.DoesNotExist:
        pass
    else:
        ent = obj.get_type_display()
        ext = ''

    return "{ent} {ext}".format(ent=ent, ext=ext)

