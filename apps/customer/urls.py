from django.conf.urls import url
from .views import LogoutView, LoginView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(),  name="auth_login"),
    url(r'^logout/$', LogoutView.as_view(), name='auth_logout'),
]
