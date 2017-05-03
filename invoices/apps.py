# -*- coding:utf-8 -*-
from __future__ import unicode_literals
# Stdlib imports


# Core Django imports
from django.apps import AppConfig
from django.utils.translation import ugettext as _
# Third-party app imports

# Realative imports of the 'app-name' package

class AppsConfig(AppConfig):
    name = 'apps'
    verbose_name = u"Apps"
