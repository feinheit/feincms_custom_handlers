from django.http import Http404, HttpResponse
from feincms.utils import get_object
from feincms_handlers import NotMyJob

from .views.cbv.ajax import AjaxHandler
from .views.cbv.autolanguage import AutoLanguageHandler
from feincms.views.cbv.views import Handler as FeinCMSHandler
from .views.cbv.htmlsnapshot import HtmlSnapshotHandler

__all__ = ['AjaxHandler', 'AutoLanguageHandler', 'FeinCMSHandler',
           'HtmlSnapshotHandler', 'MasterHandler']


class MasterHandler(object):
    """ This is where you register your handlers. They will be called one after the
        other until one returns a response.
    """

    def __init__(self, handlers=None, *args, **kwargs):
        self.handlers = []
        if handlers:
            self.register(handlers)

    def _register_handler(self, handler):
        if not hasattr(handler, 'as_view'):
            raise AttributeError('Handler %s has no method "as_view". Needs one.' % handler)
        self.handlers.append(handler.as_view())

    def register(self, handlers):
        if isinstance(handlers, list):
            for h in handlers:
                self._register_handler(h)
        else:
            self._register_handler(handlers)

    def unregister(self, handler):
        self.handlers.remove(handler)


    def __call__(self, request, path=None):
        for handler in self.handlers:
            try:
                return handler.__call__(request, path)
            except (NotMyJob, Http404) as e:
                continue

        # No response until now:
        raise Http404()

    @property
    def __name__(self):
        """
        Dummy property to make this handler behave like a normal function.
        This property is used by django-debug-toolbar
        """
        return self.__class__.__name__
