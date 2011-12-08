from feincms.views.base import Handler
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from feincms.module.page.models import Page
from feincms_handlers import NotMyJob

class PageIdFallbackHandler(Handler):
    """ This Handler is used if you have static links within your content.
        You can append a get parameter 'p' with the page id. The CMS will
        find the page even if it has been moved.
    """

    def __call__(self, request, path=None):
        if not request.GET.get('p', None):
            raise NotMyJob(self)
        try:
            page = get_object_or_404(Page, pk=request.GET.get('p', None))
        except ValueError:
            raise Http404
        return redirect(page)

handler = PageIdFallbackHandler()