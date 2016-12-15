import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.middleware.thread_user import CuserMiddleware
from core.constants import SELECT_DEFAULT, STATUS_MODEL1, ENABLED
from core.queryset import AuditableManager

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class TimeStampedModel(models.Model):
    date_created = models.DateTimeField(
        blank=True, null=True, editable=False, auto_now_add=True,
        verbose_name=_('date created'))
    date_modified = models.DateTimeField(
        blank=True, null=True, editable=False, auto_now=True,
        verbose_name=_('date modified'))
    created_by = models.ForeignKey(
        AUTH_USER_MODEL, editable=False, null=True,
        related_name="%(app_label)s_%(class)s_created_by",
        verbose_name=_('current user'))
    modified_by = models.ForeignKey(
        AUTH_USER_MODEL, editable=False, null=True,
        related_name="%(app_label)s_%(class)s_modified_by")
    
    def save(self, *args, **kwargs):
        if self.id:
            self.modified_by = CuserMiddleware.get_user()
            self.date_modified = datetime()
        else:
            self.created_by = CuserMiddleware.get_user()
            self.date_created = datetime()
            kwargs['force_insert'] = False
        super(TimeStampedModel, self).save(*args, **kwargs)

    def delete(self, force=False, *args, **kwargs):
        self.is_deleted = True
        self.save()
        if force:
            super(TimeStampedModel, self).delete(*args, **kwargs)
            
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.date_modified = datetime()
    #     else:
    #         self.date_created = datetime()
    #         kwargs['force_insert'] = False
    #     super(TimeStampedModel, self).save(*args, **kwargs)
    #
    # def delete(self, force=False, *args, **kwargs):
    #     self.is_deleted = True
    #     self.save()
    #     if force:
    #         super(TimeStampedModel, self).delete(*args, **kwargs)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    uid = models.UUIDField(editable=False, default=uuid.uuid4)
    class Meta:
        abstract = True


class StatusModel(models.Model):
    is_deleted = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True


class StatusCurrent(models.Model):
    current_status = models.CharField(
        max_length=10, choices=SELECT_DEFAULT + STATUS_MODEL1, default=ENABLED)

    class Meta:
        abstract = True


class ManagerBase(models.Model):
    current = AuditableManager()
    objects = models.Manager()

    class Meta:
        abstract = True


class BaseModel(ManagerBase, TimeStampedModel, StatusModel):
    class Meta:
        abstract = True

class BaseModel2(ManagerBase, UUIDModel, TimeStampedModel, StatusModel):
    class Meta:
        abstract = True


