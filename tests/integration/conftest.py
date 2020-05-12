import os
import shutil
import tempfile
from contextlib import contextmanager
from mock import mock

import pytest
from google.cloud import storage


@pytest.fixture(scope="session")
def chdir():
    @contextmanager
    def _chdir(path):
        orig = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(orig)

    return _chdir


@pytest.fixture(scope="session")
def project_dir(chdir):
    projects_dir = os.path.join(os.path.dirname(__file__), "..", "data", "projects")

    @contextmanager
    def _project_dir(name):
        tmp_dir = tempfile.mkdtemp()
        try:
            src_dir = os.path.join(projects_dir, name)
            dst_dir = os.path.join(tmp_dir, name)
            shutil.copytree(src_dir, dst_dir)
            with chdir(dst_dir):
                yield dst_dir
        finally:
            shutil.rmtree(tmp_dir)

    return _project_dir


@pytest.fixture
def gcs_credentials():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "test.json"


@pytest.fixture
def gcs_bucket(gcs_credentials):
    storage_client = mock.create_autospec(storage.Client)
    mock_bucket = mock.create_autospec(
        spec=storage.Bucket(storage_client, "gcspypi2-test"), spec_set=True,
    )
    mock_blob = mock.create_autospec(storage.Blob)

    storage_client.get_bucket.return_value = mock_bucket

    # def handle_get_data(path):
    #     print(path)

    mock_bucket.get_blob.side_effect = mock_blob

    yield mock_bucket
