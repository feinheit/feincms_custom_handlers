#coding=utf-8
from feincms_handlers import NotMyJob
from django.template import Template
import urllib

from feincms.views.cbv.views import Handler
from feincms.module.page.models import Page

class HtmlSnapshotHandler(Handler):
    """
    Handler for Google's _escaped_fragment_ crawl request
    """
    def dispatch(self, request, *args, **kwargs):
        escaped_fragment = request.GET.get('_escaped_fragment_', None)
        if not escaped_fragment:
            raise NotMyJob('escapedfragment')
        setattr(request, 'escaped_fragment', urllib.unquote(escaped_fragment))
        return super(HtmlSnapshotHandler, self).dispatch(request, *args, **kwargs)


    def get_template_names(self):
        templates = super(HtmlSnapshotHandler, self).get_template_names()
        if not isinstance(templates, list):
            if isinstance(templates, tuple):
                templates = [t for t in templates]
            elif isinstance(templates, Template):
                templates = [templates]

        templates.insert(0, 'snapshot_' + templates[0])
        return templates