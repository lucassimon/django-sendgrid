# -*- coding:utf-8 -*-
from __future__ import unicode_literals

# Stdlib imports
import os
import sendgrid
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
from sendgrid.helpers.mail import *

# Imports from your apps
from .models import Invoice
from ssendgrid.models import EmailSendgrid

fake = Factory.create('pt_BR')


def generate_invoice(request):
    """
    """

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

    send = EmailSendgrid.objects.create(
        content_type=ct,
        object_id=invoice.pk,
        email='lucassrod@gmail.com',
        subject=subject,
        event='initiated'
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body="This is a simple text email body.",
        from_email="Teste Django <testdjango@djangoapp.com>",
        reply_to=['teste@djangoteste.com'],
        to=["lucassrod@gmail.com"],
    )

    msg.categories = ['teste']

    msg.extra_headers = {'INVOICE_CODE': '{}'.format(invoice.pk)}

    msg.custom_args = [
        {'invoice_code': '{}'.format(invoice.pk)},
        {'content_type': '{}'.format(ct.pk)},
        {'code': '{}'.format(send.code)},
    ]

    msg.send()

    response = HttpResponse()

    return response
