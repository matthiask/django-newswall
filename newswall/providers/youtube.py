"""
Youtube Provider
================

Get all video uploads for specific channel

Create project at Google Developers Console:
https://console.developers.google.com/

and request an API key.

Remember to enable "YouTube Data API v3" from APIs & Auth > APIs


Required configuration keys::
    {
    "provider": "newswall.providers.youtube",
    "channel_id": "...",
    "api_key": "..."
    }
"""

import urllib
from datetime import datetime

try:
    import json
except ImportError:
    # maintain compatibility with Django < 1.7
    from django.utils import simplejson as json

from providers.base import ProviderBase


class Provider(ProviderBase):
    def update(self):
        playlist_id_query = 'https://www.googleapis.com/youtube/v3/channels?' \
                            'part=contentDetails&id=%s&key=%s' % \
                            (self.config['channel_id'], self.config['api_key'])
        file_a = urllib.urlopen(playlist_id_query)
        playlist_response = json.loads(file_a.read())
        playlist_id = playlist_response['items'][0]['contentDetails']\
            ['relatedPlaylists']['uploads']

        query = "https://www.googleapis.com/youtube/v3/playlistItems?" \
                "part=snippet&playlistId=%s&key=%s" % \
                (playlist_id, self.config['api_key'])

        file_b = urllib.urlopen(query)
        raw = file_b.read()
        response = json.loads(raw)

        for entry in response['items']:
            snippet = entry['snippet']
            video_id = snippet['resourceId']['videoId']
            video_url = 'https://www.youtube.com/watch?v=%s' % video_id
            link = video_url
            self.create_story(
                link,
                title=snippet.get('title'),
                body=snippet['description'],
                image_url=snippet['thumbnails']['maxres'].get('url'),
                timestamp=datetime.strptime(
                    snippet['publishedAt'], '%Y-%m-%dT%H:%M:%S.000Z'
                ),
            )
