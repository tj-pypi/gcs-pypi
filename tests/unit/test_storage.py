try:
    from unittest import mock
    from unittest.mock import MagicMock, PropertyMock, patch
except ImportError:
    import mock
    from mock import MagicMock, PropertyMock, patch

import pytest

from gcspypi2.package import Package
from gcspypi2.storage import GCSStorage


@pytest.mark.skip("Fix with mock data")
def test_secret_in_gcs_key(secret):
    from google.cloud import storage

    storage_client = mock.create_autospec(storage.Client)
    mock_bucket = mock.create_autospec(storage.Bucket)
    mock_blob = mock.create_autospec(storage.Blob)

    mock_bucket.return_value = mock_blob
    bucket_mock = MagicMock(spec=mock_bucket)
    name = PropertyMock(return_value="gcspypi2-test")
    type(bucket_mock).name = name
    bucket_mock.get_blob.return_value = MagicMock(key=[secret])
    storage_client.get_bucket.return_value = bucket_mock
    bucket_mock.reload = MagicMock()

    mock_bucket.get_blob.return_value = mock_blob

    with patch("google.cloud.storage.Client", return_value=storage_client):
        storage = GCSStorage("appstrakt-pypi", secret)
        package = Package("test-0.1.0", [])

    assert secret in storage._object(package, "index.html").key
    assert storage.acl == "publicRead"


@pytest.mark.skip("Fix with mock data")
def test_private_gcs_key(private):
    from google.cloud import storage

    storage_client = mock.create_autospec(storage.Client)
    mock_bucket = mock.create_autospec(storage.Bucket)
    mock_blob = mock.create_autospec(storage.Blob)

    storage_client.get_bucket.return_value = mock_bucket

    mock_bucket.get_blob.return_value = mock_blob

    with patch("google.cloud.storage.Client", return_value=storage_client):
        storage = GCSStorage("appstrakt-pypi", private=private)

    assert storage.acl == "private"
