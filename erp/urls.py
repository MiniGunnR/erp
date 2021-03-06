from django.conf.urls import url, include
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    url(r'^', include('core.urls', namespace='core')),

    url(r'^attendance/', include('attendance.urls', namespace='attendance')),

    url(r'^billing/', include('billing.urls', namespace='billing')),

    url(r'^admin/', admin.site.urls),

    url(r'^requisition/', include('requisition.urls', namespace='requisition')),

    url(r'^msgs/', include('msgs.urls', namespace='msgs')),

    url(r'^inv/', include('inv.urls', namespace='inv')),

    url(r'^ticket/', include('ticket.urls', namespace='ticket')),

    url(r'^europarts/', include('europarts.urls', namespace='europarts')),

    # url(r'^euro/', include('euro.urls', namespace='euro')),

    url(r'^knitwear/', include('knitwear.urls', namespace='knitwear')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
