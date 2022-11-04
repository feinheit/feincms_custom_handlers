from django.template import Template
from feincms.module.page.models import Page
from feincms.views import Handler

from feincms_handlers import NotMyJob


class AjaxHandler(Handler):
    """
    Handler for Ajax sub-page requests.
    """

    def dispatch(self, request, *args, **kwargs):
        if not (request.is_ajax() or request.GET.get("ajax", False)):
            raise NotMyJob("ajax")
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        templates = super().get_template_names()
        if not isinstance(templates, list):
            if isinstance(templates, tuple):
                templates = [t for t in templates]
            elif isinstance(templates, Template):
                templates = [templates]

        templates.insert(0, "ajax_" + templates[0])
        return templates
