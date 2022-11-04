""" This is for FeinCMS >= 1.5. For older versions use the legacy module.

Usage Example:

from feincms_handlers import handlers

handler = handlers.MasterHandler([handlers.AjaxHandler, handlers.FeinCMSHandler])

urlpatterns += patterns('',
    url(r'^$', handlers.FeinCMSHandler.as_view(), name='feincms_home'),
    url(r'^(.*)/$', handler, name='feincms_handler'),
)


"""


class NotMyJob(Exception):
    def __init__(self, author):
        self.author = author

    def __str__(self):
        return repr(self.author)
