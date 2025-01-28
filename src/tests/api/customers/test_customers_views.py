import pytest
from django.shortcuts import reverse
from rest_framework.status import HTTP_201_CREATED

from database.customers.models import Customer
from database.users.models import AppUser
from tests import utils
from tests.database.departments.factories import DepartmentFactory
from tests.database.organizations.factories import OrganizationFactory
from tests.database.tenants.factories import Tenant2UserFactory, TenantFactory


@pytest.mark.django_db
def test_create_department_customer(authenticated_api_client):
    authenticated_api_client.cookies.load({"tenant_id": "1"})
    Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=1, domain="mytest"),
        user=AppUser.objects.all().first(),
    )
    utils.set_schema("mytest")
    OrganizationFactory.create(id=1, tenant_id=1)
    DepartmentFactory.create(id=1, tenant_id=1)
    request_body = {
        "department": 1,
    }
    response_body = {
        "department": 1,
        "id": 1,
    }

    response = authenticated_api_client.post(
        reverse("customer-list"),
        request_body,
        format="json",
    )
    assert Customer.objects.all().count() == 1

    assert response.status_code == HTTP_201_CREATED
    assert response.json() == response_body

    utils.set_schema("public")
    assert Customer.objects.all().count() == 0
