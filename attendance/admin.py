from django.contrib import admin

from .models import Attn, Leave, OffDay

admin.site.register(Attn)
admin.site.register(Leave)
admin.site.register(OffDay)
