from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .models import Requisition, Item, Vendor, Company

admin.site.register(Company)

class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    readonly_fields = ('amount',)

class RequisitionAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/disable_extra_save_buttons.css',
                    'css/admin_style.css')
        }

    inlines = [
        ItemInline,
    ]
    fields = ('issue_date', 'company', 'created_by', 'department', 'vendor', 'total')
    readonly_fields = ('total',)

    list_display = ('created_by', 'created', 'total', 'view_button')
    list_per_page = 100

    search_fields = ['created_by__username', 'created_by__first_name', 'created_by__last_name']

    def view_button(self, obj):
        return "<a href='{url}' target='_blank'>View</a>".format(url=obj.view_requisition())
    view_button.allow_tags = True
    view_button.short_description = 'Column description'

    # def response_add(self, request, obj, post_url_continue="../%s/"):
    #     if not '_continue' in request.POST:
    #         return HttpResponseRedirect(reverse("requisition:req-detail-view", args=(obj.pk,)))
    #     else:
    #         return super(RequisitionAdmin, self).response_add(request, obj, post_url_continue)
    #
    # def response_change(self, request, obj):
    #     if not '_continue' in request.POST:
    #         return HttpResponseRedirect(reverse("requisition:req-detail-view", args=(obj.pk,)))
    #     else:
    #         return super(RequisitionAdmin, self).response_change(request, obj)

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        # if not change or not instance.created_by:
        #     instance.created_by = user
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return instance

admin.site.register(Requisition, RequisitionAdmin)

admin.site.register(Vendor)
admin.site.register(Item)
