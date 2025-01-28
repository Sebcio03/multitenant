import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tests.database.users.factories import AppUserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client():
    user = AppUserFactory.create()
    token, _ = Token.objects.get_or_create(user=user)
    client = APIClient(
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )
    return client
