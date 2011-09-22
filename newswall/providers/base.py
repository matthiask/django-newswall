from newswall.models import Story


class ProviderBase(object):
    def __init__(self, source, config):
        self.source = source
        self.config = config

    def update(self):
        raise NotImplementedError
