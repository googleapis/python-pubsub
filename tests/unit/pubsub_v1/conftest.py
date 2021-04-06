import google.auth.credentials
import mock
import pytest


@pytest.fixture
def creds():
    yield mock.Mock(spec=google.auth.credentials.Credentials)
