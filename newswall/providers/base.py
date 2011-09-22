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

        return Story.objects.get_or_create(object_url=object_url,
            defaults=defaults)
