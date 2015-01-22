from django.core.files.storage import get_storage_class
from django.utils.functional import SimpleLazyObject

from storages.backends.s3boto import S3BotoStorage


StaticRootS3BotoStorage       = lambda: S3BotoStorage(location='static')
StaticRootCachedS3BotoStorage = lambda: CachedS3BotoStorage(location='static')
MediaRootS3BotoStorage        = lambda: S3BotoStorage(location='media')
ThumbRootS3BotoStorage        = lambda: S3BotoStorage(location='')


class CachedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, and gzip the remote version.
    """
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
