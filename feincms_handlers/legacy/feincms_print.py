from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from feincms.module.page.models import Page
from feincms.views.base import Handler

class PrintHandler(Handler):
    """ This handler handles print previews.
        It requires a print_... template for every FeinCMS base template.
    """

    def __call__(self, request, path=None):
        if not request.GET.get('print', False):
            raise Http404
        print('PRINT HANDLER')
        return self.build_response(request,
            Page.objects.best_match_for_path(path or request.path, raise404=True))


    def render(self, request, page):
        context = request._feincms_extra_context
        print_template = 'print_%s' % page.template.path
        context['feincms_page'] = page

        return render_to_response(print_template,
            context_instance=RequestContext(request, context))


handler = PrintHandler()