# -*- coding:utf-8 -*-
from __future__ import unicode_literals

# Stdlib imports
import datetime

# Core Django imports
from django.views.generic import (
    CreateView,
    TemplateView,
    ListView,
    DetailView,
    View
)
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Count
# Third-party app imports
from dateutil.relativedelta import relativedelta

# Imports from your apps

from ssendgrid.models import EmailSendgrid


class Dashboard(
    TemplateView
):

    # permission_required = 'accounts.can_access_administration'

    # permission_denied_message = _(u'Acesso proibido para esta operação!')

    # login_url = reverse_lazy('auths:login')

    template_name = 'dashboard/index.html'


    def get_context_data(self, *args, **kwargs):
        context = super(Dashboard, self).get_context_data(
            *args,
            **kwargs
        )

        context['title'] = 'Área principal'
        context['description'] = (
            'Principais informações do sendgrid'
        )

        now = datetime.date.today()

        month_ago = now - relativedelta(month=1)

        context['emails'] = EmailSendgrid.objects.filter(
            modified__gte=month_ago
        )

        return context

    def post(self, request, *args, **kwargs):

        context = self.get_context_data()

        start_date = datetime.datetime.strptime(
            request.POST.get('start_date'),
            "%d/%m/%Y"
        ).date()

        end_date = datetime.datetime.strptime(
            request.POST.get('end_date'),
            "%d/%m/%Y"
        ).date()

        context['form_start_date'] = start_date
        context['form_end_date'] = end_date

        return render(request, self.template_name, context)


class NotAllowed(TemplateView):

    template_name = 'errors/403.html'
