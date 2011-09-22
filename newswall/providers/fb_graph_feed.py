"""
Facebook Graph Feed API Provider
================================

This provider needs `offline_access` permission.

See here how to get an access token with all permissions:
http://liquid9.tv/blog/2011/may/12/obtaining-permanent-facebook-oauth-access-token/

Required configuration keys::

    {
    "provider": "newswall.providers.fb_graph_feed",
    "object": "FEINHEIT",
    "from_id": "239846135569",
    "access_token": "..."
    }
"""

from datetime import datetime
import facebook

from newswall.providers.base import ProviderBase


class Provider(ProviderBase):
    def update(self):
        graph = facebook.GraphAPI(self.config['access_token'])
        response = graph.get_object(u'%s/feed/' % self.config['object'])

        from_id = self.config['from_id']

        for entry in response['data']:
            if entry['from']['id'] != from_id:
                continue

            if 'to' in entry: # messages
                continue

            if 'actions' not in entry:
                continue

            self.create_story(entry['actions'][0]['link'], # comment or like
                title=entry.get('name') or entry.get('message') or entry.get('story', u''),
                body=entry.get('message', u''),
                image_url=entry.get('picture', u''),
                timestamp=datetime.strptime(entry['created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                )
