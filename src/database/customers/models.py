from django.db import models

from database.departments.models import Department
from database.tenants.models import SubTenantModel


class Customer(SubTenantModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
