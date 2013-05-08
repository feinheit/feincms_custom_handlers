#coding=utf-8
from django.conf.urls import patterns, include, url

from feincms_handlers import handlers

handler = handlers.MasterHandler([handlers.AjaxHandler, handlers.FeinCMSHandler])

urlpatterns = patterns('',
    url(r'^$', handlers.FeinCMSHandler.as_view(), name='feincms_home'),
    url(r'^(.*)/$', handler, name='feincms_handler'),
)