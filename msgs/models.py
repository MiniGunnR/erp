from django.db import models
from utils.models import Timestamped
from django.contrib.auth.models import User


class Thread(Timestamped):
    user1 = models.ForeignKey(User, related_name='my_thread_1')
    user2 = models.ForeignKey(User, related_name='my_thread_2')

    user1_read = models.BooleanField(default=False)
    user2_read = models.BooleanField(default=False)

    def __str__(self):
        return "{user1} -- {user2}".format(user1=self.user1, user2=self.user2)

    class Meta:
        ordering = ['-updated']


class Message(Timestamped):
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(User, related_name='messages_sent')
    text = models.TextField()
    receiver = models.ForeignKey(User, related_name='messages_received')

    def __str__(self):
        return "{author} -> {receiver}".format(author=self.author, receiver=self.receiver)

    class Meta:
        ordering = ['created']

