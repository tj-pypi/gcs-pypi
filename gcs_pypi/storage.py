import logging
import os

from google.cloud import storage
from google.resumable_media import InvalidResponse

from gcs_pypi.package import Index

log = logging.getLogger()


class GCSStorage(object):
    """Abstraction for storing package archives and index files in a GCS bucket."""

    def __init__(self, bucket, secret=None, bare=False, private=False, profile=None):
        self.client = storage.Client()
        self.bucket = bucket
        self.secret = secret
        self.index = "" if bare else "index.html"
        self.acl = "private" if private else "publicRead"

    def _object(self, package, filename):
        path = "%s/%s" % (package.directory, filename)
        try:
            return self.client.get_bucket(self.bucket).get_blob(
                "%s/%s" % (self.secret, path) if self.secret else path
            )
        except AttributeError:
            return self.client.get_bucket(self.bucket).blob(
                "%s/%s" % (self.secret, path) if self.secret else path
            )

    def get_index(self, package):
        try:
            html = (
                self._object(package, self.index).download_as_string().decode("utf-8")
            )
            return Index.parse(html)
        except InvalidResponse:
            return Index([])

    def put_index(self, package, index):
        self._object(package, self.index).upload_from_string(
            data=index.to_html(), content_type="text/html", predefined_acl=self.acl,
        )

    def put_package(self, package, dist_path=None):
        for filename in package.files:
            path = os.path.join(dist_path or "dist", filename)
            log.debug("Uploading file `{}`...".format(path))
            with open(path, mode="rb") as f:
                self._object(package, filename).upload_from_file(
                    file_obj=f,
                    content_type="application/x-gzip",
                    predefined_acl=self.acl,
                )
