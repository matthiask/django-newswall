from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import dates, View
from django.forms.models import model_to_dict

from .models import Source, Story
from .mixin import NewswallMixin, JSONResponseMixin

try:
    from towel import paginator
except ImportError:
    from django.core import paginator


__all__ = (
    'ArchiveIndexView', 'YearArchiveView', 'MonthArchiveView',
    'DayArchiveView', 'DateDetailView', 'SourceArchiveIndexView')


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


class FeedDataView(JSONResponseMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return super(FeedDataView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = Story.objects.active()
        clean_data = []
        for item in data:
            clean_item = model_to_dict(item)
            clean_data.append(clean_item)

        context = {
            'stories': clean_data,
        }
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())
