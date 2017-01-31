from django.shortcuts import render
import requests
import simplejson as json


def attendance(request):
    return render(request, "attendance/attendance.html")


def select_by_date(request):
    date = '20170101'
    payload = {'date': date}
    r = requests.get('http://172.16.16.172/php/mdb.php', params=payload)
    for item in r.json():
        print(item)
    return render(request, "attendance/select_by_date.html")


def select_by_month(request):
    response = []

    if request.method == "POST":
        for num in range(1, 32):
            year = request.POST.get('year')
            month = request.POST.get('month')

            if num < 10:
                day = '0' + str(num)
            else:
                day = str(num)

            date = str(year) + str(month) + str(day)

            payload = {'date': date}
            r = requests.get('http://172.16.16.172/php/mdb.php', params=payload)

    return render(request, "attendance/select_by_month.html", { "response": response })

