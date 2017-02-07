from django.contrib import admin

from .models import Department, Profile, Company, Designation

admin.site.register(Department)
admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Designation)
