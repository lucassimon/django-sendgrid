# -*- coding:utf-8 -*-
from __future__ import unicode_literals

# Stdlib imports
import logging
# Core Django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
# Third-party app imports
from faker import Factory
from sgbackend import SendGridBackend
# Imports from your apps
from .models import Invoice
from ssendgrid.models import EmailSendgrid

fake = Factory.create('pt_BR')


def generate_invoice(request):
    """
    """

    send_ok = send_mail(
        "Your Subject",
        "This is a simple text email body.",
        "Yamil Asusta <hello@yamilasusta.com>",
        ["lucassrod@gmail.com"]
    )

    invoice = Invoice.objects.create(
        price=fake.pyint()
    )

    ct = ContentType.objects.get(
        app_label='invoices',
        model='invoice'
    )

    subject = 'Fatura criada {} as {}'.format(
        invoice.code,
        invoice.created
    )

    EmailSendgrid.objects.create(
        content_type=ct,
        object_id=invoice.pk,
        email='lucassrod@gmail.com',
        subject=subject,
        event='initiated'
    )

    msg = EmailMessage(
        subject=subject,
        body="Hello, %username% This is a simple text email body.",
        from_email="Teste Django <testdjango@djangoapp.com>",
        to=["lucassrd@gmail.com"],
        headers={"Reply-To": "support@sendgrid.com"}
    )

    # Replace substitutions in sendgrid template
    msg.substitutions = {'%username%': 'Lucas Simon'}

    msg.categories = ['teste', 'development']

    msg.extra_headers = {'EXTRA_HEADER': 'VALUE'}

    mail = SendGridBackend()._build_sg_mail(msg)

    response = HttpResponse()

    return response
