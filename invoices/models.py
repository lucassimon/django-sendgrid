# -*- coding:utf-8 -*-
from __future__ import unicode_literals
# Stdlib imports
import uuid
# Core Django imports
from django.db import models
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
# Third-party app imports
from django_extensions.db.models import (
    TimeStampedModel
)
# Imports from your apps


class Invoice(TimeStampedModel):
    """
    """

    code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    price = models.IntegerField(
        verbose_name='Valor em centavos',
    )

    class Meta:

        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturas'
