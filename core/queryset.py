from django.db import models


class AuditableQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(is_deleted=True)


class AuditableManager(models.Manager):
    def get_queryset(self):
        return AuditableQueryset(model=self.model, using=self._db,
                                 hints=self._hints)

    def active(self):
        return self.get_queryset().active()
