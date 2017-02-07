from django.contrib import admin

from .models import Product, List, CarPart

admin.site.register(CarPart)

class ProductAdmin(admin.TabularInline):
    model = Product
    extra = 0


class ListAdmin(admin.ModelAdmin):
    inlines = [
        ProductAdmin
    ]

admin.site.register(List, ListAdmin)
