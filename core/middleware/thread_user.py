from __future__ import unicode_literals
import threading
from django.conf import settings


class CuserMiddleware(object):

    __users = {}

    def process_request(self, request):

        self.__class__.set_user(request.user)

    def process_response(self, request, response):
        self.__class__.del_user()
        return response

    def process_exception(self, request, exception):
        self.__class__.del_user()

    @classmethod
    def get_user(cls, default=None):
        return cls.__users.get(threading.current_thread(), default)

    @classmethod
    def set_user(cls, user):
        if isinstance(user, str):
            user = settings.AUTH_USER_MODEL.objects.get(username=user)
        cls.__users[threading.current_thread()] = user

    @classmethod
    def del_user(cls):
        cls.__users.pop(threading.current_thread(), None)