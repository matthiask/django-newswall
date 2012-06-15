from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


class SourceManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)


class Source(models.Model):
    is_active = models.BooleanField(_('is active'), default=True)
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    ordering = models.IntegerField(_('ordering'), default=0)

    data = models.TextField(_('configuration data'), blank=True)

    class Meta:
        ordering = ['ordering', 'name']
        verbose_name = _('source')
        verbose_name_plural = _('sources')

    objects = SourceManager()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('newswall_source_detail', (), {'slug': self.slug})


class StoryManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)


class Story(models.Model):
    # Mandatory data
    is_active = models.BooleanField(_('is active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), default=datetime.now)
    object_url = models.URLField(_('object URL'), unique=True)
    source = models.ForeignKey(Source, related_name='stories',
        verbose_name=_('source'))

    # story fields
    title = models.CharField(_('title'), max_length=1000)
    author = models.CharField(_('author'), max_length=100, blank=True)
    body = models.TextField(_('body'), blank=True,
        help_text=_('Content of the story. May contain HTML.'))
    image_url = models.CharField(_('image URL'), max_length=1000, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('story')
        verbose_name_plural = _('stories')

    objects = StoryManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.object_url
