#coding=utf-8
from django.conf.urls.defaults import patterns, include, url

from feincms.views.cbv.views import Handler
from views.cbv.ajax import AjaxHandler
handler = Handler.as_view()
ajax_handler = AjaxHandler.as_view()

urlpatterns = patterns('',
    url(r'^$', handler, name='feincms_home'),
    url(r'^(.*)/$', ajax_handler, name='feincms_handler'),
)