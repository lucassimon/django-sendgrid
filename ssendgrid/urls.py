# -*- coding:utf-8 -*-
from __future__ import unicode_literals
# Stdlib imports

# Core Django imports
from django.conf.urls import url, include
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

# Third-party app imports

# Imports from your apps
from .views import (
    SendgridHook,
    EmailView
)

urlpatterns = [
    url(
        r'^$',
        EmailView.as_view(),
        name='emails-list'
    ),
    url(
        r'^sendgrid_callback/$',
        SendgridHook.as_view()
    ),
]
