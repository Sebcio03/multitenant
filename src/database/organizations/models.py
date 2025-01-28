from django.db import models

from database.tenants.models import SubTenantModel, Tenant


class Organization(SubTenantModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
