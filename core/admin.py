from django.contrib import admin

from .models import Department, Profile, Company, Designation


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'proximity_id',)
    list_editable = ['proximity_id']

admin.site.register(Profile, ProfileAdmin)

admin.site.register(Department)
admin.site.register(Company)
admin.site.register(Designation)
