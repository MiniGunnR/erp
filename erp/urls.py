from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('core.urls', namespace='core')),

    url(r'^billing/', include('billing.urls', namespace='billing')),

    url(r'^admin/', admin.site.urls),

    url(r'^requisition/', include('requisition.urls', namespace='requisition')),
]
