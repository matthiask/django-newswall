from django.core.management.base import NoArgsCommand
from django.utils import importlib

try:
    import json
except ImportError:
    # maintain compatibility with Django < 1.7
    from djanto.utils import simplejson as json

from newswall.models import Source


class Command(NoArgsCommand):
    help = 'Updates all active sources'

    def handle_noargs(self, **options):
        for source in Source.objects.filter(is_active=True):
            config = json.loads(source.data)
            provider = importlib.import_module(
                config['provider']).Provider(source, config)
            provider.update()
