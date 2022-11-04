This module allows to include custom feincms handlers. Major use cases are ajax-responses that
only return a small part of the page or mobile versions of the site.

There is a Legacy version for FeinCMS < 1.5. The main version is for FeinCMS >= 1.5

Currently the following handlers are included:
----------------------------------------------

CBV Handlers:
+++++++++++++

Ajax
----
Allows to ajaxify a FeinCMS website. If a request is Ajax it renders tempates prefixed with ``ajax_``.

The ajax handler can use history.js (https://github.com/browserstate/history.js) for client-side HTML history.

Checkout this gist for ajaxifying your webiste: https://gist.github.com/854622


HtmlSnapshot
------------
For making your Ajax-Site Google crawlable. According to this standard:
https://developers.google.com/webmasters/ajax-crawling/docs/getting-started

The handler will look for a template prefixed with ``snapshot_`` and add the
``_escaped_fragment_`` part as an attribute ``escaped_fragment`` to the request.
You can then render additional content within that template to show a flat
representation of your ajax web site.


Autolanguage
------------
Automatically redirect to the page in the user's language if available.
Useful for Facebook tabs and places where a language nav cannot be used.
Not recommended for general use.


Legacy Handlers:
++++++++++++++++

FeinCMS Print
-------------

If the request has a GET parameter called 'print', it prefixes the base templates with 'print_'.


Page ID fallback
----------------

If the request contains a GET parameter 'p' with a Page id it redirects to that page. This can be useful
if you have to add static links to a FeinCMS page and want to make sure the page is reachable even if moved.



Usage Example:
--------------

CBV Handler:
++++++++++++

By default, the FeinCMS and the Ajax handlers are active. You can add them like this::

  urlpatterns += patterns('',
      url(r'', include('feincms_handlers.urls')),
  )

To customize the configuration add this to your ``urls.py``::

  from feincms_handlers import handlers

  handler = handlers.MasterHandler([handlers.AjaxHandler,
                                  handlers.HtmlSnapshotHandler,
                                  handlers.FeinCMSHandler])

  urlpatterns += patterns('',
      url(r'^$', handlers.FeinCMSHandler.as_view(), name='feincms_home'),
      url(r'^(.*)/$', handler, name='feincms_handler'),
  )







Legacy Handler:
+++++++++++++++
::

  from feincms_handlers import legacy

  handler = legacy.MasterHandler(['feincms_handlers.legacy.page_id_fallback.handler',
                    'feincms_handlers.legacy.feincms_print.handler',
                    feincms_handler
                  ])

  urlpatterns += patterns('',
      url(r'^$', handler, name='feincms_home'),
      url(r'^(.*)/$', handler, name='feincms_handler'),
  )
