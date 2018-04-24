from django.db import transaction


class AtomicMixin(object):
    def dispatch(self, request, *args, **kwargs):
        with transaction.atomic():
            return super(AtomicMixin, self).dispatch(request, *args, **kwargs)