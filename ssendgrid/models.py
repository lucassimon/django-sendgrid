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

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
except ImportError:  # Django < 1.9
    from django.contrib.contenttypes.generic import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType


def _new_uuid():
    """Initialisation function for reference UUID."""

    return str(uuid.uuid4())


class EmailSendgrid(TimeStampedModel):
    """
    Salva os email enviados pelo sendgrid
    """

    code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    content_type = models.ForeignKey(
        ContentType,
        null=True
    )

    object_id = models.PositiveIntegerField(null=True)

    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )

    email = models.CharField(
        _('email'),
        max_length=255
    )

    subject = models.CharField(
        _('subject'),
        max_length=255
    )

    event = models.CharField(
        _('event type'),
        max_length=32
    )

    reason = models.CharField(
        _('reason'),
        max_length=255,
        default=''
    )

    categories = models.CharField(
        _('SendGrid Categories'),
        max_length=255,
        blank=True
    )

    sg_message_id = models.CharField(
        _('SendGrid Message Id'),
        max_length=255,
        blank=True
    )

    timestamp = models.CharField(
        _('SendGrid Timestamp'),
        max_length=255,
        blank=True
    )

    smtp_id = models.CharField(
        _('SendGrid SMTP Id'),
        max_length=255,
        blank=True
    )

    ip = models.CharField(
        _('SendGrid IP'),
        max_length=255,
        blank=True
    )

    def __unicode__(self):

        return '{}, {}'.format(
            self.email,
            self.subject
        )

    __str__ = __unicode__

    class Meta:
        verbose_name = _(u'Email')
        verbose_name_plural = _(u'Emails')
