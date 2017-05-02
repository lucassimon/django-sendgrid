# -*- coding:utf-8 -*-
from __future__ import unicode_literals
# Stdlib imports

# Core Django imports
from django.conf.urls import url, include
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

# Third-party app imports

# Imports from your apps


urlpatterns = [
    url(r'^$', 'homepage', name='homepage'),
]
