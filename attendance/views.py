from django.shortcuts import render
import requests, os
from django.conf import settings


def attendance(request):
    return render(request, "attendance/attendance.html")


def select_by_date(request):
    date = '20161215'
    payload = {'date': date}
    r = requests.get('http://172.16.16.172/php/mdb.php', params=payload)

    txt = r.text.replace('null', '')
    file = os.path.join(settings.BASE_DIR, "attendance_date.txt")
    f= open(file, "w+")
    f.write(txt)
    f.close()

    return render(request, "attendance/select_by_date.html")


def select_by_month(request):
    txt = ''

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

            txt += r.text.replace('null', '')
            f= open("attendance_month.txt","w+")
            f.write(txt)
            f.close()

    return render(request, "attendance/select_by_month.html", { "txt": txt })

