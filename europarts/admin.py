from django.contrib import admin

from .models import Product, ProductList

admin.site.register(Product)
admin.site.register(ProductList)
