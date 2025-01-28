import pytest
from django.shortcuts import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from database.organizations.models import Organization
from database.users.models import AppUser
from tests import utils
from tests.database.organizations.factories import OrganizationFactory
from tests.database.tenants.factories import Tenant2UserFactory, TenantFactory
from tests.database.users.factories import AppUserFactory


@pytest.mark.django_db
def test_create_tenant_organization(authenticated_api_client):
    authenticated_api_client.cookies.load({"tenant_id": "1"})
    Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=1, domain="mytest"),
        user=AppUser.objects.all().first(),
    )
    response_body = {
        "tenant_id": 1,
        "id": 1,
    }

    utils.set_schema("mytest")
    response = authenticated_api_client.post(
        reverse("organization-list"),
        format="json",
    )
    assert Organization.objects.all().count() == 1

    assert response.status_code == HTTP_201_CREATED
    assert response.json() == response_body

    utils.set_schema("public")
    assert Organization.objects.all().count() == 0


@pytest.mark.django_db
def test_get_tenant_organizations(authenticated_api_client):
    t2u1 = Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=10, domain="mytest"),
        user=AppUser.objects.all().first(),
    )
    utils.set_schema("mytest")
    OrganizationFactory.create(tenant=t2u1.tenant)

    t2u2 = Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=1, domain="asd"),
        user=AppUserFactory.create(),
    )
    utils.set_schema("asd")
    OrganizationFactory.create(tenant=t2u2.tenant)

    response_body = [
        {
            "id": 1,
            "tenant_id": 10,
        }
    ]

    utils.set_schema("mytest")
    authenticated_api_client.cookies.load({"tenant_id": "10"})
    response = authenticated_api_client.get(
        reverse("organization-list"),
        format="json",
    )
    assert Organization.objects.count() == 1
    assert response.status_code == HTTP_200_OK
    assert response.json() == response_body
