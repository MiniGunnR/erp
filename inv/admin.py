from django.contrib import admin

from .models import *

admin.site.register(Inventory)
admin.site.register(LetterOfCredit)
admin.site.register(LCItem)
admin.site.register(YarnReceived)
admin.site.register(YarnDelivery)
admin.site.register(FabricDelivery)

