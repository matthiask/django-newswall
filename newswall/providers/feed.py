"""
RSS Feed Provider
=================

Required configuration keys::

    {
    "provider": "newswall.providers.feed",
    "source": "http://twitter.com/statuses/user_timeline/feinheit.rss"
    }
"""
from datetime import datetime
import feedparser
import time

from newswall.providers.base import ProviderBase


class Provider(ProviderBase):
    def update(self):
        feed = feedparser.parse(self.config['source'])

        for entry in feed['entries']:
            self.create_story(entry.link,
                title=entry.title,
                body=entry.description,
                timestamp=datetime.fromtimestamp(time.mktime(entry.date_parsed)),
                )
