# from django.db.models import Sum
# from django.http import HttpResponse
#
# from .models import LCItem, YarnReceived
#
# def select_lcitem(request, pk):
#     lc_item = LCItem.objects.get(id=pk)
#     qty = lc_item.quantity
#     yr_set = lc_item.yarnreceived_set.all()
#     if not yr_set.exists():
#         sum = 0
#     else:
#         sum = yr_set.aggregate(Sum('quantity'))['quantity__sum']
#     return HttpResponse(qty - sum)
#
#
# def select_yr(request, pk):
#     yr = YarnReceived.objects.get(id=pk)
#     qty = yr.quantity
#     yi_set = yr.yarnissue_set.all()
#     if not yi_set.exists():
#         sum = 0
#     else:
#         sum = yi_set.aggregate(Sum('quantity'))['quantity__sum']
#     return HttpResponse(qty - sum)
