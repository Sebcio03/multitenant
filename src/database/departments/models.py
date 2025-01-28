from django.db import models

from database.organizations.models import Organization
from database.tenants.models import SubTenantModel


class Department(SubTenantModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
