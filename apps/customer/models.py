from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, Permission)
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail
from django.db import models
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


from core import constants as core_constants
from core.utils.fields import BaseModel
from core.utils.upload_folder import upload_user_profile
from .manager import UserManager

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=40, blank=True,
                                  null=True, unique=False)
    last_name = models.CharField(max_length=40, blank=True,
                                 null=True, unique=False)
    display_name = models.CharField(_('display name'), max_length=14,
                                    blank=True, null=True, unique=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        full_name = '{0:s} {1:s}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    @property
    def name(self):
        if self.first_name:
            return self.first_name
        elif self.display_name:
            return self.display_name
        return 'You'

    def guess_display_name(self):
        """Set a display name, if one isn't already set."""
        if self.display_name:
            return

        if self.first_name and self.last_name:
            dn = "%s %s" % (self.first_name, self.last_name[0])
        elif self.first_name:
            dn = self.first_name
        else:
            dn = 'You'
        self.display_name = dn.strip()

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def get_profile(self):
        profile = UserProfile.objects.select_related('user').get(pk=self)
        return profile

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.email

    class Meta:
        abstract = True


class User(CustomUser):
    class Meta(CustomUser.Meta):
        swappable = AUTH_USER_MODEL
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'


class UserProfile(BaseModel):
    user = models.OneToOneField(
        User, primary_key=True, verbose_name='user',
        related_name="%(app_label)s_%(class)s_user")
    address = models.CharField(max_length=200, blank=True, null=True)
    document_type = models.CharField(
        max_length=20, null=True, blank=True,
        choices=core_constants.SELECT_DEFAULT + core_constants.TYPE_IDENTITY_DOCUMENT_OPTIONS)
    document_number = models.CharField(max_length=20, null=True, blank=True)
    home_phone = models.CharField(max_length=50, blank=True, null=True)
    mobile_phone = models.CharField(max_length=50, blank=True, null=True)
    logo_profile = models.ImageField(
        upload_to=upload_user_profile, blank=True, null=True)

    def __str__(self):
        return force_text(self.user.email)

    def get_full_name(self):
        return "{0}{1}".format(self.first_name, self.last_name)

    def get_user_email(self):
        return self.user.email

    def get_logo_profile_url(self):
        if self.logo_profile:
            return self.logo_profile.url
        else:
            return static('themes/img/logo/default-profile.jpg')

    def thumb(self):
        if self.profile_image:
            return format_html(u'<img src="{0:s}" width=60 height=60 />'
                               .format(self.profile_image.url))
        else:
            img = static('assets/img/uncompressed/default_profile.png')
            return format_html(
                u'<img src="{0:s}" width=60 height=60 />'.format(img))

    thumb.short_description = _('Thumbnail')
    thumb.allow_tags = True

    class Meta:
        db_table = 'user_profile'
