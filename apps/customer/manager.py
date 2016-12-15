from django.contrib.auth.models import BaseUserManager

from core.utils.funct_dates import str_datetime as datetime


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_admin=False,
                     **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        is_active = extra_fields.pop("is_active", True)
        user = self.model(email=self.normalize_email(email),
                          is_active=is_active, is_admin=is_admin,
                          last_login=datetime(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, **extra_fields)
