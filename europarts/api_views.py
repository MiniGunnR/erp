from django.http import JsonResponse

from .models import Worksheet, WorksheetRow, Inventory


def fetch_item_details(request, part_no):
    item = Inventory.objects.get(part_no=part_no)
    return JsonResponse({
        "part_no": part_no,
        "brand": item.brand,
        "type": item.type,
        "description": item.description,
        "cost_price": item.cost_price
    })


def get_past_price(request, part_no):
    rows = WorksheetRow.objects.filter(part_no=part_no)
    response = []
    for row in rows:
        response.append(row.sale_price)
    response.sort(reverse=True)
    return JsonResponse(response, safe=False)


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
