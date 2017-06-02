# from django.db import models
# from django.contrib.auth.models import User
#
# from utils.models import Timestamped
#
#
# class Employee(Timestamped):
#     user = models.OneToOneField(User)
#     employee_id = models.CharField(max_length=7, unique=True)
#
#     def __str__(self):
#         return self.employee.username
#
#
# class LeaveDays(Timestamped):
#     employee = models.ForeignKey(Employee)
#     date = models.DateField()
#
#     def __str__(self):
#         return "{user} => {date}".format(user=self.user, date=self.date)
#
#
# class Attendance(Timestamped):
#     employee = models.ForeignKey(Employee)
#     datetime = models.DateTimeField()
#     late = models.BooleanField(default=False)
#
#     def __str__(self):
#         return "{user} => {datetime}".format(user=self.user, datetime=self.datetime)
#
