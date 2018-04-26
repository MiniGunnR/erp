from __future__ import absolute_import, unicode_literals


from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email(subject, body, from_email, to, attachment):
    email = EmailMessage()
    email.subject = subject
    email.body = body
    email.from_email = from_email
    email.to = to
    email.attach_file(attachment)

    email.send()

