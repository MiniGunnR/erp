from django.db import models
from utils.models import Timestamped
from django.conf import settings


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    sip = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return "{user}'s Profile".format(user=self.user.get_full_name())

