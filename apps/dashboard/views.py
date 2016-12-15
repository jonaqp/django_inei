from django.conf import settings
from django.shortcuts import redirect

from core.mixins import TemplateLoginRequiredMixin


class IndexView(TemplateLoginRequiredMixin):
    template_name = 'dashboard/base_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
