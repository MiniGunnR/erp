from django.db import models

from utils.models import Timestamped
from django.conf import settings


class LeaveDays(Timestamped):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateField()

    def __str__(self):
        return "{user} => {date}".format(user=self.user, date=self.date)


class Attendance(Timestamped):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    datetime = models.DateTimeField()
    late = models.BooleanField(default=False)

    def __str__(self):
        return "{user} => {datetime}".format(user=self.user, datetime=self.datetime)

