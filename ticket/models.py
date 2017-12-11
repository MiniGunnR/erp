from django.db import models

from utils.models import Timestamped
from django.contrib.auth.models import User


class TicketType(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


Unattended = 'U'
Proposed = 'P'
Accepted = 'A'
Denied = 'D'

STATUS_CHOICES = (
    (Unattended, 'Unattended'),
    (Proposed, 'Solution Proposed'),
    (Accepted, 'Solution Accepted'),
    (Denied, 'Solution Denied'),
)


class Ticket(Timestamped):
    type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    details = models.TextField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=Unattended)
    created_by = models.ForeignKey(User, related_name='tickets_created', on_delete=models.CASCADE)

    solved = models.BooleanField(default=False)
    solved_by = models.ForeignKey(User, related_name='tickets_solved', blank=True, null=True, on_delete=models.CASCADE)

    denied = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.details

    def propose_solution(self, current_user):
        self.solved = True
        self.solved_by = current_user
        self.status = Proposed
        self.save()

    def deny_solution(self):
        self.solved = False
        self.denied = True
        self.status = Denied
        self.save()

    def accept_solution(self):
        self.accepted = True
        self.status = Accepted
        self.save()
