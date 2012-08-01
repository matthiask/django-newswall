from django.conf import settings
from django.contrib.syndication.views import Feed

from newswall.models import Story


class StoryFeed(Feed):
    title = getattr(settings, 'BLOG_TILE', 'Default Title')
    link = '/news/'
    description = getattr(settings, 'BLOG_DESCRIPTION', 'Default Description')

    def items(self):
        return Story.objects.active().order_by('-timestamp')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_pubdate(self, item):
        return item.timestamp
