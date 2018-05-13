from __future__ import absolute_import, unicode_literals
import os, pwd, grp, tempfile

from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import reverse
from django.test.client import RequestFactory
from wkhtmltopdf.views import PDFTemplateResponse, PDFTemplateView


@shared_task
def generate_pdf_and_send_email(template, filename, context, pk, model, subject, body, from_email, to):
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
        # filename=file_path,
        context=context,
        show_content_in_browser=False,
        cmd_options={'margin-top': 10,
                     'zoom': 1,
                     'viewport-size': '1366 x 513',
                     'show_content_in_browser': False,
                     'javascript-delay': 1000,
                     'no-stop-slow-scripts': True},
    )

    # f = open(file_path, "wb+")
    # os.chmod(file_path, 0777)
    # uid = pwd.getpwnam("michel").pw_uid
    # gid = grp.getgrnam("apache").gr_gid
    # os.chown(file_path, uid, gid)
    # f.write(response.rendered_content)
    # f.close()

    # with open(file_path, 'wb') as f:
    #     f.write(response.rendered_content)

    # attachment = os.path.join(settings.MEDIA_ROOT, file_name)

    pdf = response.rendered_content

    email = EmailMessage()
    email.subject = subject
    email.body = body
    email.from_email = from_email
    email.to = to

    email.attach('demo.pdf', pdf, 'application/pdf')

    email.send()

    return
