from django.contrib import admin

from .models import LC, LCItem, YarnRcv, YarnIssue, FabricDelivery


class LCItemInline(admin.TabularInline):
    model = LCItem
    extra = 1


class LCAdmin(admin.ModelAdmin):
    inlines = [
        LCItemInline,
    ]

admin.site.register(LC, LCAdmin)

admin.site.register(YarnRcv)

admin.site.register(YarnIssue)

admin.site.register(FabricDelivery)
