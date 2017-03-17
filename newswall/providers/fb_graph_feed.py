"""
Facebook Graph Feed API Provider
================================

This provider needs `offline_access` permission.

See here how to get an access token with all permissions:
http://liquid9.tv/blog/2011/may/12/obtaining-permanent-facebook-oauth-access-token/  # noqa

Required configuration keys::

    {
    "provider": "newswall.providers.fb_graph_feed",
    "object": "FEINHEIT",
    "from_id": "239846135569",
    "access_token": "..."
    }
"""

import urllib

from datetime import datetime

try:
    import json
except ImportError:
    # maintain compatibility with Django < 1.7
    from django.utils import simplejson as json

from newswall.providers.base import ProviderBase


class Provider(ProviderBase):
    def update(self):
        args = {'access_token': self.config['access_token']}
        query = "https://graph.facebook.com/v2.4/%s/feed?%s&fields=" \
                "full_picture,picture,name,message,story,created_time,from," \
                "likes" % (
                    self.config['object'],
                    urllib.urlencode(args),
                )
        file = urllib.urlopen(query)
        raw = file.read()
        response = json.loads(raw)

        from_id = self.config.get('from_id', None)

        for entry in response['data']:
            if from_id and entry['from']['id'] != from_id:
                continue

            if 'to' in entry:  # messages
                continue

            link = 'https://facebook.com/%s' % (
                entry['id'].replace('_', '/posts/'),
            )
            try:
                like_count = len(entry['likes'].get('data'))
            except KeyError:  # No likes
                like_count = None
            story = self.create_story(
                link,
                title=(
                    entry.get('name') or entry.get('message') or
                    entry.get('story', u'')
                ),
                body=entry.get('message', u''),
                image_url=entry.get('full_picture', u''),
                timestamp=datetime.strptime(
                    entry['created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
            )
            story[0].update_extra_data(key='FacebookLikeCount',
                                       value=like_count)
