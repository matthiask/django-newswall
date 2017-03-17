# -*- coding: utf-8 -*-
import json
from django import http
from django.core.serializers.json import DjangoJSONEncoder

from .models import Story


class NewswallMixin(object):
    """
    This mixin autodetects whether the blog is integrated through a FeinCMS
    ApplicationContent and automatically switches to inheritance2.0 if that's
    the case. Please note that FeinCMS is NOT required, this is purely for the
    convenience of FeinCMS users. The functionality for this is contained
    inside ``base_template`` and ``render_to_response``.

    Additionally, it adds the view instance to the template context
    as ``view``.
    """

    @property
    def base_template(self):
        if hasattr(self.request, '_feincms_page'):
            return self.request._feincms_page.template.path
        return 'newswall/newswall_base.html'

    def get_context_data(self, **kwargs):
        kwargs.update({'view': self})
        return super(NewswallMixin, self).get_context_data(**kwargs)

    def get_queryset(self):
        return Story.objects.active().select_related('source')

    def render_to_response(self, context, **response_kwargs):
        if 'app_config' in getattr(self.request, '_feincms_extra_context', {}):
            return self.get_template_names(), context

        return super(NewswallMixin, self).render_to_response(
            context, **response_kwargs)


class JSONResponseMixin(object):
    def render_to_response(self, context,**kwargs):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context),
                                      **kwargs)

    def get_json_response(self, content, **httpresponse_kwargs):
        """Construct an `HttpResponse` object."""
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context, cls=DjangoJSONEncoder)
