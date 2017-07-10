from django.db import models
from datetime import time
from time import strptime


class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


ATTN_TYPE_CHOICES = (
    ('N', 'Entry'),
    ('X', 'Exit'),
    ('L', 'Leave'),
)


class Attn(Timestamp):
    emp_id = models.CharField(
        max_length=10
    )
    dt = models.DateField()
    tm = models.TimeField(
        default=time(00, 00)
    )
    type = models.CharField(
        max_length=1,
        choices=ATTN_TYPE_CHOICES,
        default='N'
    )

    @property
    def late(self):
        if self.tm.hour > 9:
            return True
        elif self.tm.hour == 9 and self.tm.minute >= 30:
            return True
        else:
            return False

    def saturday(self):
        return self.dt.weekday() == 5

    def save(self, *args, **kwargs):
        try:
            Attn.objects.get(emp_id=self.emp_id, dt=self.dt, type='N')
        except Attn.DoesNotExist:
            pass
        else:
            try:
                attn = Attn.objects.get(emp_id=self.emp_id, dt=self.dt, type='X')
            except Attn.DoesNotExist:
                self.type = 'X'
            else:
                attn.delete()
                self.type = 'X'
        super(Attn, self).save(*args, **kwargs)

    def __str__(self):
        return "{emp_id} : {dt} => {tm}".format(emp_id=self.emp_id, dt=self.dt, tm=self.tm)


class Default(Timestamp):
    attribute = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return "{attribute} --> {value}".format(attribute=self.attribute, value=self.value)


class EmployeeLeave(Timestamp):
    emp_id = models.CharField(
        max_length=10,
        unique=True
    )
    sick_leave = models.SmallIntegerField()
    casual_leave = models.SmallIntegerField()

    def __str__(self):
        return "Employee: {emp_id}, SL: {sl}, CL: {cl}".format(emp_id=self.emp_id, sl=self.sick_leave, cl=self.casual_leave)


LEAVE_TYPE_CHOICES = (
    ('S', 'Sick'),
    ('C', 'Casual'),
)


class Leave(Timestamp):
    emp_id = models.CharField(
        max_length=10
    )
    date = models.DateField()
    type = models.CharField(
        max_length=1,
        choices=LEAVE_TYPE_CHOICES,
        default='S'
    )

    class Meta:
        unique_together = ('emp_id', 'date')


class OffDay(Timestamp):
    date = models.DateField()
    details = models.CharField(
        max_length=100,
        default='Day Off'
    )

