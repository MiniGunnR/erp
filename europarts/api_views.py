from django.http import JsonResponse

from .models import Worksheet


def cost_price_toggle(request, pk):
    worksheet = Worksheet.objects.get(id=pk)

    if request.method == "POST":
        worksheet.cost_price_visible = not worksheet.cost_price_visible
        worksheet.save()
        return JsonResponse({'visible': worksheet.cost_price_visible})
    else:
        return JsonResponse({'visible': worksheet.cost_price_visible})


def sale_price_toggle(request, pk):
    worksheet = Worksheet.objects.get(id=pk)

    if request.method == "POST":
        worksheet.sale_price_visible = not worksheet.sale_price_visible
        worksheet.save()
        return JsonResponse({'visible': worksheet.sale_price_visible})
    else:
        return JsonResponse({'visible': worksheet.sale_price_visible})


def total_toggle(request, pk):
    worksheet = Worksheet.objects.get(id=pk)

    if request.method == "POST":
        worksheet.total_visible = not worksheet.total_visible
        worksheet.save()
        return JsonResponse({'visible': worksheet.total_visible})
    else:
        return JsonResponse({'visible': worksheet.total_visible})
