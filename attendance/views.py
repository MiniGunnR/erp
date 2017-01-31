from django.shortcuts import render


def select_by_date(request):

    return render(request, "attendance/select_date.html")