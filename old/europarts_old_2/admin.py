from django.contrib import admin

from .models import *

admin.site.register(Brand)
admin.site.register(AutoType)
admin.site.register(AutoPart)
admin.site.register(List)
admin.site.register(Product)
admin.site.register(Quotation)
admin.site.register(QuotationCode)
admin.site.register(QuotationProduct)