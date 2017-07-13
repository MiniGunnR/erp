from django import template

register = template.Library()

from datetime import datetime

from core.models import Profile
from ..models import Attn, Leave, OffDay
from ..views import WEEKLY_OFF


@register.filter(name='fetch_attendance')
def fetch_attendance(date, emp_id):
    try:
        attn = Attn.objects.get(emp_id=emp_id, dt=date, type='N')
    except Attn.DoesNotExist:
        ent = 'ABS'
        if datetime.strptime(date, "%Y-%m-%d").weekday() == WEEKLY_OFF:
            ent = 'OFF'
    else:
        ent = attn.tm.strftime("%H:%M")
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

    if ent == 'ABS':
        ent = '<label class="label label-danger">' + ent + '</label>'
    elif ent == 'OFF':
        ent = '<label class="label label-default">' + ent + '</label>'
    else:
        if 'attn' in locals():
            if attn.late:
                ent = '<label class="label label-warning">' + ent + '</label>'
            else:
                ent = '<label class="label label-success">' + ent + '</label>'
        else:
            ent = '<label class="label label-default">' + ent + '</label>'

    if ext == 'X':
        ext = ''
    else:
        ext = '<label class="label label-primary">' + ext + '</label>'

    return "{ent} {ext}".format(ent=ent, ext=ext)


@register.filter(name='fetch_employee_name')
def fetch_employee_name(emp_id):
    try:
        obj = Profile.objects.get(proximity_id=emp_id)
    except Profile.DoesNotExist:
        name = 'Cannot retrieve name.'
    else:
        name = obj.user.get_full_name()

    return name


@register.filter(name='summary')
def summary(data):
    try:
        present = len([1 for i in data if not i[3] and not i[1] == 'OFF' and not i[1] == 'ABS'])
        late = len([1 for i in data if i[3] and not i[1] == 'OFF'])
        absent = len([1 for i in data if i[1] == 'ABS'])
    except IndexError:
        return "<label class='label label-success'>PRS: 0</label><br/>" \
               "<label class='label label-warning'>LT: 0</label><br/>" \
               "<label class='label label-danger'>ABS: 0</label>"
    return "<label class='label label-success'>PRS: {present}</label><br/>" \
           "<label class='label label-warning'>LT: {late}</label><br/>" \
           "<label class='label label-danger'>ABS: {absent}</label>".format(present=present, late=late, absent=absent)


@register.filter(name='summary_print')
def summary_print(data):
    try:
        present = len([1 for i in data if not i[3] and not i[1] == 'OFF' and not i[1] == 'ABS' and not i[1] == 'Casual' and not i[1] == 'Sick'])
        late = len([1 for i in data if i[3] and not i[1] == 'OFF'])
        absent = len([1 for i in data if i[1] == 'ABS'])
        leave = len([1 for i in data if i[1] == 'Casual' or i[1] == 'Sick'])
        weekly_holiday = len([1 for i in data if i[1] == 'OFF'])
        festival_holiday = len([1 for i in data if ':' not in i[1]]) - absent - weekly_holiday - leave
    except IndexError:
        return "<td>0</td>" \
               "<td>0</td>" \
               "<td>0</td>"
    return "<td>{present}</td>" \
           "<td>{absent}</td>" \
           "<td>{late}</td>"\
           "<td>{leave}</td>"\
           "<td>{weekly_holiday}</td>" \
           "<td>{festival_holiday}</td>".format(present=present, late=late, absent=absent, leave=leave, weekly_holiday=weekly_holiday, festival_holiday=festival_holiday)


@register.filter(name='summary2')
def summary2(data):
    try:
        present = len([1 for i in data if not i[3] and not i[1] == 'OFF' and not i[1] == 'ABS'])
        late = len([1 for i in data if i[3] and not i[1] == 'OFF'])
        absent = len([1 for i in data if i[1] == 'ABS'])
    except IndexError:
        return '<td></td>' \
               '<td></td>' \
               '<td></td>'

    response = '<td>' + str(present) + '</td>' \
               '<td>' + str(late) + '</td>' \
               '<td>' + str(absent) + '</td>'
    return response
