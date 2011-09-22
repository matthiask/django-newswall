"""
Elephantblog Entry Provider
===========================

Required configuration keys::

    {
    "provider": "newswall.providers.elephantblog"
    }
"""

from __future__ import absolute_import

from django.contrib.sites.models import Site

from elephantblog.models import Entry

from newswall.providers.base import ProviderBase


class Provider(ProviderBase):
    def update(self):
        domain = Site.objects.get_current().domain

        for entry in Entry.objects.active():
            url = 'http://%s%s' % (domain, entry.get_absolute_url())

            try:
                body = entry.richtextcontent_set.all()[0].text
            except:
                body = u''

            self.create_story(url,
                title=entry.title,
                timestamp=entry.published_on,
                body=body,
                )
