# -*- coding:utf-8 -*-
from __future__ import unicode_literals

# Stdlib imports
import json
import datetime
import sendgrid
import os

# Core Django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import (
    View, CreateView, TemplateView, ListView, DetailView
)

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.timezone import utc
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.conf import settings

# Third-party app imports
from dateutil.relativedelta import relativedelta
# Imports from your apps
from .models import EmailSendgrid


# Core Django imports


class EmailView(
    TemplateView
):

    template_name = 'ssendgrid/emails_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EmailView, self).get_context_data(
            *args,
            **kwargs
        )

        context['title'] = 'Emails enviados'
        context['description'] = (
            'Emails enviados para o sendgrid'
        )

        now = datetime.date.today()

        month_ago = now - relativedelta(month=1)

        context['emails'] = EmailSendgrid.objects.filter(
            modified__gte=month_ago
        )

        return context


class SendgridHook(View):
    state_flow = {
        # Internal: Step 0
        'initiated': (
            'received',
            'processed',
            'dropped',
            'delivered',
            'bounce',
            'open',
            'click',
            'unsubscribe',
            'spamreport'
        ),
        # Sendgrid: Step 1 - Receive
        'received': (
            'processed',
            'dropped',
            'delivered',
            'bounce',
            'open',
            'click',
            'unsubscribe',
            'spamreport'
        ),
        # Sendgrid: Step 2 - Process
        'processed': (
            'delivered',
            'bounce',
            'open',
            'click',
            'unsubscribe',
            'spamreport'
        ),
        'dropped': (),
        # Sendgrid: Step 3 - Deliver
        'delivered': ('open', 'click', 'unsubscribe', 'spamreport'),
        'bounce': (),
        # Sendgrid: Step 4 - Read
        'open': (),
        'click': (),
        'unsubscribe': (),
        'spamreport': (),
    }

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SendgridHook, self).dispatch(*args, **kwargs)

    def post(self, request):
        response = json.loads(request.body)

        email = None

        for event in response:

            if 'code' not in event.keys():
                return HttpResponse('Thanks!')

            try:
                email = EmailSendgrid.objects.get(code=event['code'])
            except Exception:
                # TODO salvar em um LOG o Erro
                raise
            except (EmailSendgrid.DoesNotExist, KeyError):
                raise

            if 'email' in event.keys():
                email.email = event.get('email')
            else:
                # TODO salvar em um LOG o Erro
                raise

            email.reason = event.get('reason', '')

            if event.get('category'):
                email.categories = ' ,'.join(
                    cat for cat in event.get('category')
                )

            if event.get('sg_message_id'):
                email.sg_message_id = event.get('sg_message_id')

            if event.get('smtp-id'):
                email.smtp_id = event.get('smtp-id')

            if event.get('smtp-id'):
                email.smtp_id = event.get('ip')

            if event.get('timestamp'):
                timestamp = datetime.datetime.fromtimestamp(
                    int(
                        event['timestamp']
                    )
                )
                if settings.USE_TZ:
                    timestamp = timestamp.utcnow().replace(tzinfo=utc)
                email.timestamp = timestamp

            try:
                current_options = self.state_flow[email.event]
                if event['event'] in current_options:
                    email.event = event['event']
                else:
                    # TODO salvar em um LOG o Erro
                    raise
            except KeyError:
                # TODO salvar em um LOG o Erro
                raise

            email.save()

        return HttpResponse('Thanks!')
