from __future__ import absolute_import, unicode_literals
import os

from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import reverse
from django.test.client import RequestFactory
from wkhtmltopdf.views import PDFTemplateResponse


@shared_task
def generate_pdf_and_send_email(template, context, pk, model, subject, body, from_email, to):
    request = RequestFactory().get(reverse('europarts:{model}_email'.format(model=model), args=[pk]))

    kw = {
        '{model}_id'.format(model=model): pk
    }
    row_model = '{model}Row'.format(model=model)
    rows = apps.get_model('europarts', row_model).objects.filter(**kw)
    context['{model}_rows'.format(model=model)] = rows
    file_name = '{model}_email.pdf'.format(model=model)

    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    response = PDFTemplateResponse(
        request=request,
        template=template,
        filename=file_path,
        context=context,
        # show_content_in_browser=False,
        # cmd_options={'margin-top': 10,
        #              'zoom': 1,
        #              'viewport-size': '1366 x 513',
        #              'show_content_in_browser': False,
        #              'javascript-delay': 1000,
        #              'no-stop-slow-scripts': True},
    )

    pdf = response.rendered_content

    email = EmailMessage()
    email.subject = subject
    if body == '':
        body = '''Dear Sir,

        Please find the attached file.

        Sincerely Yours,
        {full_name}
        '''.format(full_name=request.user.get_full_name)
    email.body = body
    email.from_email = from_email
    email.to = to

    email.attach(file_name, pdf, 'application/pdf')

    email.send()

    return
