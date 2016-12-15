from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import (
    CreateView, DeleteView, DetailView,
    ListView, TemplateView, UpdateView
)


class TemplateLoginRequiredMixin(LoginRequiredMixin, TemplateView):
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        url_name = request.resolver_match.url_name
        namespace_name = request.resolver_match.namespaces[0]
        self.text_central = "{0} {1}".format(str(url_name), str(namespace_name))
        self.path_url_create = "{0}:{1}".format(str(namespace_name), "create")
        self.path_url_update = "{0}:{1}".format(str(namespace_name), "update")
        self.path_url_delete = "{0}:{1}".format(str(namespace_name), "delete")
        self.path_url_list = "{0}:{1}".format(str(namespace_name), "list")
        return super().dispatch(request, *args, **kwargs)


class AuthListView(AuthMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["path_url_update"] = self.path_url_update
        context["path_url_delete"] = self.path_url_delete
        context["path_url_create"] = self.path_url_create
        return context


class AuthDeleteView(AuthMixin, DeleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_central"] = _("Delete Record")
        context["path_url_list"] = self.path_url_list
        return context


class AuthDetailView(AuthMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_central"] = _("Detail Record")
        context["path_url_list"] = self.path_url_list
        return context


class AuthUpdateView(AuthMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_central"] = _("Update Record")
        context["path_url_list"] = self.path_url_list
        return context


class AuthCreateView(AuthMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_central"] = _("Create Record")
        context["path_url_list"] = self.path_url_list
        return context


class AuthTemplateCreateView(AuthMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_central"] = _("Create Record")
        context["path_url_list"] = self.path_url_list
        return context
