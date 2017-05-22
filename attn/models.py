from django.db import models

from utils.models import Timestamped


class Attendance(Timestamped):
    employee_id = models.CharField(max_length=10)
    punch = models.DateTimeField()

    def __str__(self):
        return "{employee} => {date} => {time}".format(employee=self.employee_id, date=self.punch.date(), time=self.punch.time())

    class Meta:
        ordering = ['punch']
