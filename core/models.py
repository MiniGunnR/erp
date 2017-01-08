from django.db import models
from utils.models import Timestamped


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
