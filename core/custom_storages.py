from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


# from storages.backends.gs import GSBotoStorage


class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION

    # class StaticStorage(GSBotoStorage):
    #     location = str(settings.STATICFILES_LOCATION)
    #
    #
    # class MediaStorage(GSBotoStorage):
    #     location = str(settings.MEDIAFILES_LOCATION)