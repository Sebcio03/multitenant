import pytest
from django.db import connection
from django.shortcuts import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from database.departments.models import Department
from database.users.models import AppUser
from tests import utils
from tests.database.departments.factories import DepartmentFactory
from tests.database.organizations.factories import OrganizationFactory
from tests.database.tenants.factories import Tenant2UserFactory, TenantFactory


@pytest.mark.django_db
def test_create_organization_department(authenticated_api_client):
    authenticated_api_client.cookies.load({"tenant_id": "1"})
    Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=1, domain="mytest"),
        user=AppUser.objects.all().first(),
    )
    utils.set_schema("mytest")
    OrganizationFactory.create(id=1, tenant_id=1)
    request_body = {
        "organization": 1,
    }
    response_body = {
        "organization": 1,
        "id": 1,
    }

    response = authenticated_api_client.post(
        reverse("department-list"),
        request_body,
        format="json",
    )
    assert Department.objects.all().count() == 1

    assert response.status_code == HTTP_201_CREATED
    assert response.json() == response_body

    utils.set_schema("public")
    assert Department.objects.all().count() == 0


@pytest.mark.django_db
def test_get_organization_departments_from_different_tenant(authenticated_api_client):
    t2u1 = Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=10, domain="mytest"),
        user=AppUser.objects.all().first(),
    )
    Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=1, domain="eddst"),
        user=AppUser.objects.all().first(),
    )
    utils.set_schema("mytest")
    o1 = OrganizationFactory.create(tenant=t2u1.tenant, id=1)
    DepartmentFactory.create(organization_id=o1.id, id=1)
    o2 = OrganizationFactory.create(tenant=t2u1.tenant, id=2)
    DepartmentFactory.create(organization_id=o2.id, id=2)

    authenticated_api_client.cookies.load({"tenant_id": "1"})
    response = authenticated_api_client.get(
        reverse("department-list") + "?organization=2",
        format="json",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == []
    with connection.cursor() as cursor:
        cursor.execute("SHOW search_path;")
        assert cursor.fetchall() == [("eddst",)]


@pytest.mark.django_db
def test_get_organization_departments(authenticated_api_client):
    t2u1 = Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=10, domain="mytest"),
        user=AppUser.objects.all().first(),
    )
    utils.set_schema("mytest")
    o1 = OrganizationFactory.create(tenant=t2u1.tenant, id=1)
    DepartmentFactory.create(organization_id=o1.id, id=1)
    o2 = OrganizationFactory.create(tenant=t2u1.tenant, id=2)
    DepartmentFactory.create(organization_id=o2.id, id=2)

    response_body = [
        {
            "id": 2,
            "organization": 2,
        }
    ]

    authenticated_api_client.cookies.load({"tenant_id": "10"})
    response = authenticated_api_client.get(
        reverse("department-list") + "?organization=2",
        format="json",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == response_body
