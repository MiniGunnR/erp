from django.shortcuts import render

from .models import Worksheet


def home(request):
    return render(request, "europarts/home.html")


def worksheet_list(request):
    worksheets = Worksheet.objects.all()
    context = {
        "worksheets": worksheets,
    }
    return render(request, "europarts/worksheet/worksheet_list.html", context)


def worksheet_create(request):
    return render(request, "europarts/worksheet/worksheet_create.html")

