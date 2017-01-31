from django.shortcuts import render


def attendance(request):
    return render(request, "attendance/attendance.html")


def select_by_date(request):
    return render(request, "attendance/select_by_date.html")


def select_by_month(request):
    return render(request, "attendance/select_by_month.html")

