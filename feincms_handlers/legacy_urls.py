""" Add this to your urls.py """

from django.conf.urls.defaults import *

# FeinCMS Handler location:
from feincms.views.base import handler as feincms_handler

from feincms_handlers.views.legacy import handler


handler.register(feincms_handler)

urlpatterns = patterns(
    "",
    url(r"^$", handler, name="feincms_home"),
    url(r"^(.*)/$", handler, name="feincms_handler"),
)
