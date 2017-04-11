from django.shortcuts import render
from datetime import timedelta, date


def _daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


def date_range(request):
    dates = []
    if request.GET:
        start_date = date(int(request.GET.get('from_year')), int(request.GET.get('from_month')), int(request.GET.get('from_day')))
        end_date = date(int(request.GET.get('to_year')), int(request.GET.get('to_month')), int(request.GET.get('to_day')))
        for single_date in _daterange(start_date, end_date):
            dates.append([single_date, 'some data', 'some more'])
    return render(request, "payroll/date_range.html", {"dates": dates})
