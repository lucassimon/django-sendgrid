# -*- coding:utf-8 -*-
from __future__ import unicode_literals
# Stdlib imports

# Core Django imports
from django.contrib.sitemaps import Sitemap


# Third-party app imports

# Imports from your apps
from .models import Model


class ModelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Model.objects.all()
