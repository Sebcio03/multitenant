from django.core.exceptions import PermissionDenied
from django.db import connection
from django.http import HttpRequest
from rest_framework.authentication import TokenAuthentication

from database.tenants.models import Tenant2User
from database.users.models import AppUser

EXCLUDE_ENDPOINTS = ["/api/users/", "/api/tenants/"]


class TokenAuthenticationWithTenantValidation(TokenAuthentication):
    def validate_user_access2tenant(self, request: HttpRequest, user: AppUser) -> None:
        if any(request.path.startswith(i) for i in EXCLUDE_ENDPOINTS):
            return

        tenant_id = request.COOKIES.get("tenant_id")
        if tenant_id is None or not user.is_authenticated:
            raise PermissionDenied("Access denied")

        tenant = Tenant2User.objects.filter(tenant_id=tenant_id, user=user).first()
        if not tenant:
            raise PermissionDenied("Access denied")

        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path TO {tenant.tenant.domain};")

    def authenticate(self, request: HttpRequest) -> (AppUser, str):
        with connection.cursor() as cursor:
            cursor.execute("SET search_path TO public;")

        auth = super().authenticate(request)
        if not auth:
            return None
        self.validate_user_access2tenant(request, auth[0])
        return auth
