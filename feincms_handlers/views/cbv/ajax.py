#coding=utf-8

from feincms.views.cbv.views import Handler
from feincms.module.page.models import Page

class AjaxHandler(Handler):
    """
    Handler for Ajax sub-page requests.
    """
       
    def get(self, request, *args, **kwargs):
        if request.is_ajax() or request.GET.get('ajax', False): 
            return self.ajax_handler(request, *args, **kwargs)
        else:
            return self.handler(request, *args, **kwargs)
 
    def ajax_handler(self, request, path=None, *args, **kwargs):
        self.page = Page.objects.for_request(request, raise404=True, best_match=True, setup=False)
        template_prefix = getattr(self, 'template_prefix', 'ajax_')
        self.template_name = '%s%s' % (template_prefix, self.page.template.path),
        response = self.prepare()
        if response:
            return response

        response = self.render_to_response(self.get_context_data())
        return self.finalize(response)