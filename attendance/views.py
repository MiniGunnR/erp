from django.shortcuts import render


def select_date(request):
    return render(request, "attendance/select_date.html")