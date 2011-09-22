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

Hvae a look at the following blog post to find out how to generate such an
access token:
<http://liquid9.tv/blog/2011/may/12/obtaining-permanent-facebook-oauth-access-token/>


RSS Feed
--------

The RSS feed provider can take any RSS or Atom feed (in fact anything parseable
by ``feedparser`` and turn the stories into news entries::

    {
    "provider": "newswall.providers.feed",
    "source": "http://twitter.com/statuses/user_timeline/unsocialrider.rss"
    }


Twitter RSS Feed
----------------

Specialized RSS feed provider which does not write anything into the story
body but only fills the story title. Title and content are always the same in
Twitter's RSS feed anyway::

    {
    "provider": "newswall.providers.twitter",
    "user": "feinheit"
    }
