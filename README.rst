========
Newswall
========

This is my version of a Tumblelog. Why, you might ask? Because I can.


Installation and usage
======================

1. Add ``newswall`` to ``INSTALLED_APPS``
2. Run ``./manage.py migrate newswall`` (or ``syncdb``, if you prefer to work
   without South)
3. Add the following line to your ``urls.py``::

    url(r'^news/', include('newswall.urls')),

4. Add news providers by create a few ``Source`` objects through Django's
   admin panel
5. Create a cronjob running ``./manage.py update_newswall`` periodically (i.e.
   every hour)


Providers
=========

``newswall`` has a few bundled providers, those being:


Elephantblog
------------

Adds news entries for every active entry in a elephantblog installation on the
same website. No additional configuration required (or possible). Add the
following JSON configuration to the ``Source`` entry::

    {"provider": "newswall.providers.elephantblog"}


Facebook Graph Feed
-------------------

This provider adds news entries for every wall post on a Facebook page. The
wall posts are accessed through the Graph API; you'll need a copy of the Python
Facebook SDK somewhere on your Python path. You'll need an access token with
``offline_access`` permission for this provider. Required configuration
follows::

    {"provider": "newswall.providers.fb_graph_feed",
    "object": "FEINHEIT",      // used to construct the Graph request URL
    "from_id": "239846135569", // used to filter stories created by the
                               // object referenced above, ignores stories
                               // sent by others
    "access_token": "..."
    }

We suggest to use App Access Tokens to query the Facebook Page feed, because they don't expire.
To get an App Access Token, simply open this URL with your browser, after
filling in the required fields (the all caps words)::

    https://graph.facebook.com/oauth/access_token?client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&grant_type=client_credentials

More infos according the App Access Tokens can be found on the official Facebook documentation:
<https://developers.facebook.com/docs/opengraph/using-app-tokens/>

To obtain the "from_id" configuration parameter, you can query the Facebook Open Graph
API Backend with your Browser::

    https://graph.facebook.com/OBJECT

f.e.:
<https://graph.facebook.com/FEINHEIT>

RSS Feed
--------

The RSS feed provider can take any RSS or Atom feed (in fact anything parseable
by ``feedparser`` and turn the stories into news entries::

    {
    "provider": "newswall.providers.feed",
    "source": "http://twitter.com/statuses/user_timeline/unsocialrider.rss"
    }


Twitter API Feed
----------------

Required: tweepy

Usage:

Create a twitter app.
You'll find the consumer_key/secret on the detail page.
Because this is a read-only application, you can create
your oauth_token/secret directly on the bottom of the app detail page.

Required configuration keys::

    {
    "provider": "newswall.providers.twitter",
    "user": "feinheit",
    "consumer_key": "...",
    "consumer_secret": "...",
    "oauth_token": "...",
    "oauth_secret": "..."
    }
