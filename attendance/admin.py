from django.contrib import admin

from .models import Attn, Leave, OffDay, EmployeeLeave, Default

admin.site.register(Attn)
admin.site.register(Leave)
admin.site.register(OffDay)
admin.site.register(EmployeeLeave)
admin.site.register(Default)
