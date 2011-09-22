import feedparser

from newswall.providers.base import ProviderBase


class Provider(ProviderBase):
    def update(self):
        print 'Should update from feed %s' % self.config['source']
