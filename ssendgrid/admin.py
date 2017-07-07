# -*- coding:utf-8 -*-
from __future__ import unicode_literals
# Stdlib imports


# Core Django imports
from django.contrib import admin
from django.utils.translation import ugettext as _

# Third-party app imports
from mptt.admin import MPTTModelAdmin
# Realative imports of the 'app-name' package

from .models import EmailSendgrid

admin.site.register(EmailSendgrid, MPTTModelAdmin)
