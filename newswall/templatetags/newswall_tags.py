from django import template

from newswall.models import Source, Story


register = template.Library()


@register.assignment_tag
def newswall_sources():
    return Source.objects.active()


@register.assignment_tag
def newswall_archive_months():
    return Story.objects.active().dates('timestamp', 'month', 'DESC')
