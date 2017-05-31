import calendar, copy, os, csv, requests

from datetime import date, datetime, timedelta

from django import forms
from django.http import HttpResponseRedirect, Http404
from django.utils.dates import MONTHS
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings


from .models import Attn, Leave, OffDay
from .forms import OffDayFrom, OffDayTo, OffDayName

EMPLOYEES = [
    '0001010702',
    '0001010701',
]

WEEKLY_OFF = calendar.SATURDAY


def employees(request):
    emp_ids = EMPLOYEES

    c = {
        "emp_ids": emp_ids,
        "year": datetime.now().year,
    }
    return render(request, "attendance/employees.html", c)


def month_summary(request, month, year):
    # convert variables to int
    month = int(month)
    year = int(year)

    month_dates = []  # create an empty list for dates of the month

    # loop over a tuple of lists containing (day, weekday)
    for day in calendar.Calendar().itermonthdays2(year, month):
        if day[0] != 0:  # do the following to tuples that have a valid date
            day = list(day)
            day.insert(1, 'W')  # insert second item to list that says if workday or off day
            if day[2] == WEEKLY_OFF:  # if day is off day
                day[1] = 'O'
                day[2] = 'Weekly Off Day'
            else:
                day_0_date = date(year, month, day[0])

                if day_0_date > datetime.now().date():
                    day[1] = 'W'
                    day[2] = 'Future Day'
                else:
                    day[1] = 'W'
                    day[2] = 'Office Day'

                try:
                    off_day = OffDay.objects.get(date=day_0_date)
                except OffDay.DoesNotExist:
                    pass
                else:
                    day[1] = 'O'
                    day[2] = off_day.details

            month_dates.append(day)
    print(month_dates)

    employee_attendances = []

    for employee in EMPLOYEES:
        employee_data = copy.deepcopy(month_dates)
        for item in employee_data:
            dt = date(year, month, item[0])

            if dt <= datetime.now().date():
                try:
                    attn = Attn.objects.get(emp_id=employee, dt=dt, type='N')
                except Attn.DoesNotExist:
                    if item[1] == 'O':
                        entry = 'OFF'
                    else:
                        entry = 'ABS'
                    # check if employee has leave
                    try:
                        lv = Leave.objects.get(emp_id=employee, date=dt)
                    except Leave.DoesNotExist:
                        pass
                    else:
                        entry = lv.get_type_display()
                else:
                    entry = attn.tm.strftime('%H:%M')

                try:
                    attn = Attn.objects.get(emp_id=employee, dt=dt, type='X')
                except Attn.DoesNotExist:
                    exit = 'X'
                else:
                    exit = attn.tm.strftime('%H:%M')

                item[1] = entry
                item[2] = exit

            # don't show any data for future dates
            elif dt > datetime.now().date() and item[1] == 'W':
                item[1] = '-'
                item[2] = ''

        employee_attendances.append({employee: employee_data})

    # print(employee_attendances)

    c = {
        "month_dates": month_dates,
        "employee_attendances": employee_attendances,
    }
    return render(request, "attendance/month_summary.html", c)


def employee_summary(request, employee_id, year):
    year = int(year)

    cal = calendar.Calendar(firstweekday=6).yeardatescalendar(year, width=12)

    months = []

    pres = []
    late = []
    off = []
    leave = []
    weekly_off = []
    absent = []

    for month in range(1, 13):
        months.append(calendar.month_abbr[month])

        attns = Attn.objects.filter(emp_id=employee_id, dt__year=year, dt__month=month, type='N')
        pres.append(attns.count())
        late.append(len([1 for i in attns if i.late]))

        matrix = calendar.monthcalendar(year,month)
        saturdays = sum(1 for x in matrix if x[calendar.SATURDAY] != 0)
        working_sats = len([i for i in attns if i.saturday()])
        saturdays -= working_sats
        weekly_off.append(saturdays)

        offs = OffDay.objects.filter(date__month=month)
        off.append(offs.count())

        leaves = Leave.objects.filter(date__month=month)
        leave.append(leaves.count())

        days_in_month = calendar.monthrange(year, month)[1]
        current_month = date.today().month
        if month == current_month:
            remaining_leaves = leaves.filter(date__day__gt=date.today().day).count()
            remaining_offs = offs.filter(date__gt=date.today()).count()
            remaining_sats = len([1 for i in range(date.today().day + 1, days_in_month + 1) if date.today() == 5])
            future_days = days_in_month - date.today().day - remaining_leaves - remaining_offs - remaining_sats

        if month > current_month:
            absent.append(0)
        elif month == current_month:
            absent.append(days_in_month - attns.count() - saturdays - leaves.count() - offs.count() - future_days)
        else:
            absent.append(days_in_month - attns.count() - saturdays - leaves.count() - offs.count())

    c = {
        "cal": cal,
        "emp_id": employee_id,

        "months": months,

        "pres": pres,
        "late": late,
        "off": off,
        "leave": leave,
        "weekly_off": weekly_off,
        "absent": absent,
    }

    return render(request, "attendance/employee_summary.html", c)


def off_day_entry(request):
    if request.method == "POST":
        from_form = OffDayFrom(request.POST)
        to_form = OffDayTo(request.POST)
        day_name = OffDayName(request.POST)

        if from_form.is_valid() and to_form.is_valid() and day_name.is_valid():
            from_date = date(int(request.POST.get('from_year')), int(request.POST.get('from_month')), int(request.POST.get('from_date')))
            to_date = date(int(request.POST.get('to_year')), int(request.POST.get('to_month')), int(request.POST.get('to_date')))

            if to_date < from_date:
                raise forms.ValidationError('Start date cannot be later than the end date.', code='invalid')

            diff = (to_date - from_date).days

            for i in range(diff + 1):
                off_day = from_date + timedelta(i)
                OffDay.objects.create(date=off_day, details=request.POST.get('details'))
            return HttpResponseRedirect(reverse('attendance:action'))
    else:
        from_form = OffDayFrom()
        to_form = OffDayTo()
        day_name = OffDayName()
    c = {
        "from_form": from_form,
        "to_form": to_form,
        "day_name": day_name,
    }
    return render(request, "attendance/off_day_entry.html", c)


def action(request):
    return render(request, "attendance/action.html")


def pull(request):
    if request.method == "POST":
        date = "{year}{month}{day}".format(year=request.POST.get('year'), month=request.POST.get('month'), day=request.POST.get('day'))
        return HttpResponseRedirect(reverse('attendance:select_by_date', args=(date,)))

    months = []
    for month_num, month in MONTHS.items():
        months.append(("%02d" % month_num, month))

    days = [x for x in range(1, 32)]
    days = ["%02d" % x for x in days]

    c = {
        "months": months,
        "days": days,
    }
    return render(request, "attendance/pull.html", c)


def select_by_date(request, date):
    """ Downloads all attendance entries from date till now
    :param request:
    :param date: 20170101
    :return: Returns a page with a download link which downloads a populate.csv file in media/attendance/
    """
    date = str(date)
    payload = {'date': date}
    r = requests.get('http://172.16.16.172/php/mdb.php', params=payload)

    file = os.path.join(settings.BASE_DIR, "media", "attendance", "populate.csv")

    with open(file,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows(r.json())

    return HttpResponseRedirect(reverse('attendance:populate'))


def populate(request):
    """ Populates the database with attendances from populate.csv
    :param request:
    :return: Redirects to attendance home after populating database
    """
    with open(os.path.join(settings.BASE_DIR, 'media', 'attendance', 'populate.csv')) as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                st = row[0].split(", ")
            except IndexError:
                raise Http404('Cannot create variable st')
            else:
                if len(st) == 3:
                    obj, created = Attn.objects.get_or_create(
                        emp_id=st[0],
                        dt=datetime.strptime(st[1], "%Y%m%d"),
                        tm=datetime.strptime(st[2], "%H%M%S")
                        )
                else:
                    raise Http404('Length of st is not 3')

    return HttpResponseRedirect(reverse('attendance:pull'))

