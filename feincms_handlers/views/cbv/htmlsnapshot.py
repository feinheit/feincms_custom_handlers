from urllib.parse import unquote

from django.template import Template
from django.utils.translation import get_language
from feincms.module.page.models import Page
from feincms.views import Handler

from feincms_handlers import NotMyJob


class HtmlSnapshotHandler(Handler):
    """
    Handler for Google's _escaped_fragment_ crawl request
    Requires the slug to be unique for each language.

    """

    def dispatch(self, request, *args, **kwargs):
        escaped_fragment = request.GET.get("_escaped_fragment_", None)
        if not escaped_fragment:
            raise NotMyJob("escapedfragment")
        escaped_fragment = unquote(escaped_fragment)
        setattr(request, "escaped_fragment", escaped_fragment)
        page_model = self.page_model
        pages = page_model.objects.filter(slug=escaped_fragment)
        page = None
        if len(pages) == 1:
            page = pages[0]
        elif len(pages) > 1 and hasattr(page_model, "language"):
            current_lang = get_language()
            for p in pages:
                if p.language == current_lang:
                    page = p
                    break
            if page == None:
                page = pages[0]

        setattr(request, "snapshot_page", page)
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        templates = super().get_template_names()
        if not isinstance(templates, list):
            if isinstance(templates, tuple):
                templates = [t for t in templates]
            elif isinstance(templates, Template):
                templates = [templates]

        templates.insert(0, "snapshot_" + templates[0])
        return templates
