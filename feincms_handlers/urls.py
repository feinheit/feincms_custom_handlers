from django.conf.urls import patterns
from django.urls import path, re_path

from feincms_handlers import handlers


handler = handlers.MasterHandler(
    [
        handlers.AjaxHandler,
        # handlers.HtmlSnapshotHandler,
        handlers.FeinCMSHandler,
    ]
)

urlpatterns = patterns(
    "",
    path("", handlers.FeinCMSHandler.as_view(), name="feincms_home"),
    re_path(r"^(.*)/$", handler, name="feincms_handler"),
)
