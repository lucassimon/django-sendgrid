# -*- coding:utf-8 -*-
from __future__ import unicode_literals
# Stdlib imports


# Core Django imports
from django import forms
from django.utils.translation import ugettext as _
# Third-party app imports

# Realative imports of the 'app-name' package
from .models import Scheduling


class DashboardCustomerServiceForm(forms.Form):

    start_date = forms.DateField()
    end_date = forms.DateField()

    class Meta:
        fields = '__all__'
        help_texts = {
            'start_date': _(
                _(u'Data Inicial.')
            ),
            'end_date': _(
                _(u'Data Final.')
            ),
        }

        widgets = {
            'start_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                },
            ),
            'end_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                },
            ),
        }