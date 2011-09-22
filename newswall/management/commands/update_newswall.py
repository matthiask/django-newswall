from django.core.management.base import NoArgsCommand
from django.utils import importlib, simplejson

from newswall.models import Source


class Command(NoArgsCommand):
    help = 'Updates all active sources'

    def handle_noargs(self, **options):
        for source in Source.objects.filter(is_active=True):
            config = simplejson.loads(source.data)
            provider = importlib.import_module(config['provider']).Provider(source, config)
            provider.update()
