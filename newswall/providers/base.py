from datetime import date, timedelta

from newswall.models import Story


class ProviderBase(object):
    def __init__(self, source, config):
        self.source = source
        self.config = config

    def update(self):
        raise NotImplementedError

    def create_story(self, object_url, **kwargs):
        defaults = {'source': self.source}
        defaults.update(kwargs)

        if defaults.get('title'):
            if Story.objects.filter(
                    title=defaults.get('title'),
                    timestamp__gte=date.today() - timedelta(days=3),
                    ).exists():
                defaults['is_active'] = False

        return Story.objects.get_or_create(object_url=object_url,
            defaults=defaults)
