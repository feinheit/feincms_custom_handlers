#coding=utf-8
from django.http import HttpResponseRedirect
from django.utils import translation
from feincms.views import Handler
from feincms.module.page.models import Page

class AutoLanguageHandler(Handler):
    """
    This handler checks if a feinCMS page exists in the user's language
    and redirects to that page. Useful if a language selection menu is not
    used and the user arrives on a translated page. (e.g. for a Facebook tab)

    Usage:
        autolanguage_handler = AutoLanguageHandler.as_view()

        urlpatterns += patterns('',
            url(r'^$', autolanguage_handler, name='feincms_home'),
            url(r'^(.*)/$', autolanguage_handler, name='feincms_handler'),
        )
    """

    def handler(self, request, *args, **kwargs):
        self.page = Page.objects.for_request(request, raise404=True,
                                             best_match=True, setup=False)

        language = translation.get_language()
        if self.page.language[:2] != language[:2]:
            try:
                page = self.page.get_translation(language)
            except Page.DoesNotExist:
                try:
                    page = self.page.get_translation(language[:2])
                except Page.DoesNotExist:
                    pass
                else:
                    return HttpResponseRedirect(page.get_absolute_url())
            else:
                return HttpResponseRedirect(page.get_absolute_url())

        response = self.prepare()
        if response:
            return response

        response = self.render_to_response(self.get_context_data())
        return self.finalize(response)
