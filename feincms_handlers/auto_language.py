#coding=utf-8

from feincms.views.cbv.views import Handler
from feincms.module.page.models import Page

class AutoLanguageHandler(Handler):
    """
    This handler checks if a feinCMS page exists in the user's language
    and redirects to that page. Useful if a language selection menu is not
    used and the user arrives on a translated page. (e.g. for a Facebook tab)
    """

    def handler(self, request, *args, **kwargs):
        self.page = Page.objects.for_request(request, raise404=True, best_match=True, setup=False)
        response = self.prepare()
        if response:
            return response

        response = self.render_to_response(self.get_context_data())
        return self.finalize(response)
