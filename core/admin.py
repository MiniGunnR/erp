from django.contrib import admin

from .models import Department, Profile, Company, Designation
from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
    save_on_top = True

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'proximity_id',)
    list_editable = ['proximity_id']
    save_on_top = True

admin.site.register(Profile, ProfileAdmin)

admin.site.register(Department)
admin.site.register(Company)
admin.site.register(Designation)
