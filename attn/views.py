from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.dates import MONTHS
from django.conf import settings

import calendar, csv, os, requests
from datetime import time, datetime

from utils.func import month_string_to_number

from .models import Attendance
from core.models import Profile


def _mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)


def home(request):
    now = datetime.now()
    print(now.month, now.year)
    c = {
        "month": 'May',
        "year": now.year,
    }
    return render(request, "attn/home.html", c)


def employee_list(request):
    profiles = Profile.objects.all()
    now = datetime.now()
    c = {
        "profiles": profiles,
        "now": now,
    }
    return render(request, "attn/employee_list.html", c)


def month_summary(request, month, year):
    if request.method == "POST":
        month = request.POST.get("month_selector", month)
        year = request.POST.get("year_selector", year)
        return HttpResponseRedirect(reverse('attn:month_summary', args=(month, year)))

    month_num = month_string_to_number(month)
    object_list = Attendance.objects.filter(punch__month=month_num, punch__year=int(year))
    month_name = calendar.month_name[month_num]
    cal = calendar.Calendar()

    dates = []
    for date in cal.itermonthdays(int(year), int(month_num)):
        dates.append(date)
    while 0 in dates:
        dates.remove(0)
    month_days = len(dates)

    employee_list = Profile.objects.values_list('proximity_id', flat=True)

    rows = []
    for employee in employee_list:
        rows.append([employee, dates[:], []])
    for row in rows:
        employee_id = row[0]
        row_objs = object_list.filter(employee_id=employee_id)
        days = {}
        late_count = 0
        present_count = 0
        for obj in row_objs:
            if obj.punch.day in days:
                existing_punch = days[obj.punch.day]
                if len(existing_punch) == 2:
                    raise ValueError('More than two values in a punch tuple is not allowed! {} {}'.format(employee_id, obj.punch.date()))
                existing_punch += (obj.punch.time().strftime("%H:%M"),)
                days[obj.punch.day] = existing_punch
            else:
                days[obj.punch.day] = (obj.punch.time().strftime("%H:%M"),)

        date_count = []
        for obj in row_objs:
            if obj.punch.day not in date_count:
                if obj.punch.time() > time(9, 30):
                    late_count += 1
                else:
                    present_count += 1
                date_count.append(obj.punch.day)

        row[1] = [days.get(x, ('ABS', 'ABS')) for x in row[1]]
        absent_count = month_days - present_count - late_count
        row[2] = [present_count, late_count, absent_count]

    months = []
    for month_num, month in MONTHS.items():
        months.append(month)

    c = {
        "rows": rows,
        "dates": dates,
        "month_name": month_name,
        "object_list": object_list,
        "year": year,
        "months": months,
    }
    return render(request, "attn/month_summary.html", c)


def employee_summary(request, employee_id, year):
    attendances = Attendance.objects.filter(punch__year=int(year), employee_id=employee_id)
    cal = calendar.Calendar()

    dates = []
    for date in range(1, 32):
        dates.append(date)

    attn_year = {}
    summary_dict = {}
    for month_num, month in MONTHS.items():
        attn_year[month_num] = []
        for date in cal.itermonthdays(int(year), int(month_num)):
            attn_year[month_num].append(date)
        while 0 in attn_year[month_num]:
            attn_year[month_num].remove(0)
        month_days = len(attn_year[month_num])

        days = {}
        for attendance in attendances:
            attn_day = attendance.punch.day
            attn_month = attendance.punch.month
            if attn_day in days and attn_month == month_num:
                existing_punch = days[attn_day]
                if len(existing_punch) == 2:
                    raise ValueError('More than two values in a punch tuple is not allowed! {} {}'.format(employee_id, attendance.punch.date()))
                existing_punch += (attendance.punch.time().strftime("%H:%M"),)
                days[attn_day] = existing_punch
            elif attn_day not in days and attn_month == month_num:
                days[attn_day] = (attendance.punch.time().strftime("%H:%M"),)
        attn_year[month_num] = [days.get(x, ('ABS', 'X')) for x in attn_year[month_num]]

        late_count = 0
        present_count = 0
        date_count = []
        for obj in attendances.filter(punch__month=month_num):
            if obj.punch.day not in date_count:
                if obj.punch.time() > time(9, 30):
                    late_count += 1
                else:
                    present_count += 1
                date_count.append(obj.punch.day)
        summary_dict[month_num] = [present_count, late_count, month_days - present_count - late_count]

    c = {
        "employee_id": employee_id,
        "year": year,
        "dates": dates,
        "attn_year": attn_year,
        "summary_dict": summary_dict,
    }
    return render(request, "attn/employee_summary.html", c)


def year_summary(request, year):
    months = []
    for month_num, month in MONTHS.items():
        months.append(month)

    profiles = Profile.objects.all()

    employees = {}
    for employee in profiles:
        employees[employee.proximity_id] = {}

        for month_num, month in MONTHS.items():
            attn_obj = Attendance.objects.filter(employee_id=employee.proximity_id, punch__year=year, punch__month=month_num)
            month_sum = []
            late = 0
            attn_count = attn_obj.count()
            month_days = calendar.monthrange(int(year), month_num)[1]
            absent = month_days - attn_count
            for attn in attn_obj:
                if attn.punch.time() > time(9, 30):
                    late += 1
            present = attn_count - late
            month_sum.append(present)
            month_sum.append(late)
            month_sum.append(absent)

            employees[employee.proximity_id][month_num] = month_sum
    print(employees)
    c = {
        "months": months,
        "employees": employees,
    }
    return render(request, "attn/year_summary.html", c)


def action(request):
    if request.method == "POST":
        date = "{year}{month}{day}".format(year=request.POST.get('year'), month=request.POST.get('month'), day=request.POST.get('day'))
        return HttpResponseRedirect(reverse('attn:select_by_date', args=(date,)))

    months = []
    for month_num, month in MONTHS.items():
        months.append(("%02d" % month_num, month))

    days = [x for x in range(1, 32)]
    days = ["%02d" % x for x in days]

    c = {
        "months": months,
        "days": days,
    }
    return render(request, "attn/action.html", c)


def populate(request):
    """ Populates the database with attendances from populate.csv
    :param request:
    :return: Redirects to attendance home after populating database
    """
    with open(os.path.join(settings.BASE_DIR, 'media', 'attendance', 'populate.csv')) as f:
        reader = csv.reader(f)
        for row in reader:
            row = row.split(",")
            obj, created = Attendance.objects.get_or_create(
                employee_id=row[0],
                punch=datetime.strptime(row[1].strip(), "%Y%m%d %H%M%S"),
                )
            attns = Attendance.objects.filter(employee_id=row[0], punch__date="{}-{}-{}".format(obj.punch.year, '%02d' % obj.punch.month, '%02d' % obj.punch.day))
            attn_count = attns.count()
            # The following block removes all attendance except last and first one
            if attn_count > 2:
                for attn in attns:
                    if attn == attns.first() or attn == attns.last():
                        pass
                    else:
                        attn.delete()

    return HttpResponseRedirect(reverse('attn:action'))


def select_by_date(request, date):
    """ Downloads all attendance entries from date till now
    :param request:
    :param date: 20170101
    :return: Returns a page with a download link which downloads a populate.csv file in media/attendance/
    """
    date = str(date)
    payload = {'date': date}
    r = requests.get('http://172.16.16.172/php/mdb.php', params=payload)

    rs = [
        ['apple'],
        ['banana']
    ]
    file = os.path.join(settings.BASE_DIR, "media", "attendance", "populate.csv")

    with open(file,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows(r.json())

    # txt = r.text.replace('null', '')
    # file = os.path.join(settings.BASE_DIR, "media", "attendance", "populate.csv")
    #
    # f = open(file, "w+")
    # f.write(txt)
    # f.close()

    return HttpResponseRedirect(reverse('attn:populate'))

