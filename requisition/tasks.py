from __future__ import absolute_import, unicode_literals
import os

from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import reverse
from django.test.client import RequestFactory
from wkhtmltopdf.views import PDFTemplateResponse

from core.models import Mail
from django.contrib.auth.models import User
from .models import QuotationRequest


@shared_task
def generate_pdf_and_send_email(template, context, pk, model, subject, body, from_email, to):
    request = RequestFactory().get(reverse('requisition:{model}_email'.format(model=model), args=[pk]))
    user = User.objects.get(username='tarik')

    kw = {
        '{model}_id'.format(model=model): pk
    }
    row_model = '{model}Item'.format(model=model)
    rows = apps.get_model('requisition', row_model).objects.filter(**kw)
    parent = apps.get_model('requisition', model).objects.get(id=pk)
    context['{model}_rows'.format(model=model)] = rows
    file_name = '{model}_email.pdf'.format(model=model)

    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    response = PDFTemplateResponse(
        request=request,
        template=template,
        filename=file_path,
        context=context,

    )

    pdf = response.rendered_content

    email = EmailMessage()
    email.subject = subject
    email.body = body
    email.from_email = from_email
    email.to = to

    email.attach(file_name, pdf, 'application/pdf')

    try:
        email.send()
    except:
        pass
    else:
        # Mail.objects.create(
        #     owner           = user,
        #     to_email        = to,
        #     from_email      = from_email,
        #     subject         = subject,
        #     content_object  = QuotationRequest.objects.get(id=pk),
        #     body            = body,
        # )
        pass
    return
