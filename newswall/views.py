from django.shortcuts import get_object_or_404
from django.views.generic import dates

from newswall.models import Source, Story

try:
    from towel import paginator
except ImportError:
    from django.core import paginator


__all__ = ('ArchiveIndexView', 'YearArchiveView', 'MonthArchiveView', 'DayArchiveView',
    'DateDetailView', 'SourceArchiveIndexView')


class NewswallMixin(object):
    """
    This mixin autodetects whether the blog is integrated through an
    ApplicationContent and automatically switches to inheritance2.0
    if that's the case.

    Additionally, it adds the view instance to the template context
    as ``view``.

    This requires at least FeinCMS v1.5.
    """

    def get_context_data(self, **kwargs):
        kwargs.update({'view': self})
        return super(NewswallMixin, self).get_context_data(**kwargs)

    def get_queryset(self):
        return Story.objects.active().select_related('source') #.transform(entry_list_lookup_related)

    def render_to_response(self, context, **response_kwargs):
        if 'app_config' in getattr(self.request, '_feincms_extra_context', {}):
            return self.get_template_names(), context

        return super(NewswallMixin, self).render_to_response(
            context, **response_kwargs)


class ArchiveIndexView(NewswallMixin, dates.ArchiveIndexView):
    paginator_class = paginator.Paginator
    paginate_by = 20
    date_field = 'timestamp'
    template_name_suffix = '_archive'
    allow_empty = True


class YearArchiveView(NewswallMixin, dates.YearArchiveView):
    paginator_class = paginator.Paginator
    paginate_by = 20
    date_field = 'timestamp'
    make_object_list = True
    template_name_suffix = '_archive'


class MonthArchiveView(NewswallMixin, dates.MonthArchiveView):
    paginator_class = paginator.Paginator
    paginate_by = 20
    month_format = '%m'
    date_field = 'timestamp'
    template_name_suffix = '_archive'


class DayArchiveView(NewswallMixin, dates.DayArchiveView):
    paginator_class = paginator.Paginator
    paginate_by = 20
    month_format = '%m'
    date_field = 'timestamp'
    template_name_suffix = '_archive'


class DateDetailView(NewswallMixin, dates.DateDetailView):
    paginator_class = paginator.Paginator
    paginate_by = 20
    month_format = '%m'
    date_field = 'timestamp'

    def get_queryset(self):
        return Story.objects.active()


class SourceArchiveIndexView(ArchiveIndexView):
    template_name_suffix = '_archive'

    def get_queryset(self):
        self.source = get_object_or_404(Source, slug=self.kwargs['slug'])

        queryset = super(SourceArchiveIndexView, self).get_queryset()
        return queryset.filter(source=self.source)

    def get_context_data(self, **kwargs):
        return super(SourceArchiveIndexView, self).get_context_data(
            source=self.source,
            **kwargs)
