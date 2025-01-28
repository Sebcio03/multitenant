import pytest
from django.apps import apps
from django.db import connection
from django.shortcuts import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from database.tenants.models import SubTenantModel, Tenant
from database.users.models import AppUser
from tests.database.tenants.factories import Tenant2UserFactory, TenantFactory
from tests.database.users.factories import AppUserFactory


@pytest.mark.django_db
def test_create_tenant(authenticated_api_client):
    all_subtenant_models = [
        (model.objects.model._meta.db_table,)
        for model in apps.get_models()
        if issubclass(model, SubTenantModel)
    ]
    request_body = {"domain": "mytest"}
    response_body = {
        "domain": "mytest",
        "tenant_id": 1,
    }

    response = authenticated_api_client.post(
        reverse("tenant-list"),
        request_body,
        format="json",
    )
    assert Tenant.objects.filter(domain="mytest").count() == 1

    with connection.cursor() as cursor:
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'mytest';")
        assert cursor.fetchall() == all_subtenant_models

    assert response.status_code == HTTP_201_CREATED
    assert response.json() == response_body


@pytest.mark.django_db
def test_get_user_tenants(authenticated_api_client):
    Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=10, domain="mytest"),
        user=AppUser.objects.all().first(),
    )
    Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=1, domain="asd"),
        user=AppUserFactory.create(),
    )

    response_body = [{"tenant_id": 10, "domain": "mytest"}]

    response = authenticated_api_client.get(
        reverse("tenant-list"),
        format="json",
    )
    assert Tenant.objects.count() == 2
    assert response.status_code == HTTP_200_OK
    assert response.json() == response_body


@pytest.mark.django_db
def test_get_user_tenant_details_and_activate(authenticated_api_client):
    Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=10, domain="mytest"),
        user=AppUser.objects.all().first(),
    )
    response_body = {"tenant_id": 10, "domain": "mytest"}

    response = authenticated_api_client.get(
        reverse("tenant-detail", args=[10]),
        format="json",
    )
    assert response.cookies.get("tenant_id").value == "10"
    assert response.status_code == HTTP_200_OK
    assert response.json() == response_body


@pytest.mark.django_db
def test_get_other_user_tenant_details_and_activate(authenticated_api_client):
    Tenant2UserFactory.create(
        tenant=TenantFactory.create(tenant_id=10, domain="mytest"),
        user=AppUserFactory.create(),
    )

    response = authenticated_api_client.get(
        reverse("tenant-detail", args=[10]),
        format="json",
    )
    assert response.cookies.get("tenant_id", None) is None
    assert response.status_code == HTTP_404_NOT_FOUND
