# -*- coding: utf-8 -*-
"""
Instagram Provider
==================

Required configuration keys::
    {
    "provider": "newswall.providers.instagram",
    "username": "...",
    }

"""
from __future__ import unicode_literals
from lxml import html

import requests
import datetime

try:
    import json
except ImportError:
    # maintain compatibility with Django < 1.7
    from django.utils import simplejson as json

from newswall.providers.base import ProviderBase

SCRIPT_JSON_PREFIX = 18
SCRIPT_JSON_DATA_INDEX = 21


def get_ig_data(username):
    url = "https://www.instagram.com/{}/".format(username)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    scripts = tree.xpath('//script')
    shared_data = None

    for script in scripts:
        if script.text:
            if script.text[0:SCRIPT_JSON_PREFIX] == 'window._sharedData':
                shared_data = script.text[SCRIPT_JSON_DATA_INDEX:-1]

    if not shared_data:
        raise ValueError('Unable to get _sharedData for username "{}"'
                         .format(username))

    json_data = json.loads(shared_data)
    return json_data


class Provider(ProviderBase):

    def update(self):
        username = self.config['username']
        data = get_ig_data(self.config['username'])

        user_data = data.get('entry_data').get('ProfilePage')[0].get('user')
        user_media = user_data.get('media')['nodes']

        for obj in user_media:
            if bool(obj.get('is_video')):
                continue

            obj_id = obj.get('id')
            link = "https://www.instagram.com/{}/#{}".format(username, obj_id)
            image_url = obj.get('display_src')
            timestamp = datetime.datetime.fromtimestamp(obj.get('date'))
            caption = obj.get('caption', '')
            self.create_story(
                link, title=obj_id, body=caption, image_url=image_url,
                timestamp=timestamp
            )
