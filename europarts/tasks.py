from __future__ import absolute_import, unicode_literals
import os

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import reverse
from django.test.client import RequestFactory
from europarts.models import ChallanRow
from wkhtmltopdf.views import PDFTemplateResponse


@shared_task
def generate_pdf_and_send_email(template, filename, context, pk, model, subject, body, from_email, to, attachment):
    request = RequestFactory().get(reverse('europarts:challan_email', args=[pk]))

    kw = {
        'challan_id': pk
    }
    rows = ChallanRow.objects.filter(**kw)
    context['challan_rows'] = rows

    response = PDFTemplateResponse(
        request=request,
        template=template,
        filename=filename,
        context=context,
        show_content_in_browser=True,
        cmd_options={'margin-top': 10,
                     'zoom': 1,
                     'viewport-size': '1366 x 513',
                     'javascript-delay': 1000,
                     'no-stop-slow-scripts': True},
    )

    file_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'challan_email.pdf')
    with open(file_path, 'wb+') as f:
        f.write(response.rendered_content)

    email = EmailMessage()
    email.subject = subject
    email.body = body
    email.from_email = from_email
    email.to = to
    email.attach_file(attachment)

    email.send()

    os.remove(attachment)

    return response


