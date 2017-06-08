from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import Department, Profile, Company, Designation
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UzerAdmin(UserAdmin):
    model = User
    save_on_top = True

    def response_change(self, request, obj):
        return HttpResponseRedirect('/admin/core/profile/' + str(obj.id) + '/change/')

admin.site.unregister(User)
admin.site.register(User, UzerAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'proximity_id',)
    list_editable = ['proximity_id']
    save_on_top = True

admin.site.register(Profile, ProfileAdmin)

admin.site.register(Department)
admin.site.register(Company)
admin.site.register(Designation)
