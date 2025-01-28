import logging

from django.apps import apps
from django.core.validators import RegexValidator
from django.db import connection, models

from database.users.models import AppUser

logger = logging.getLogger(__name__)

# Based on RFC 1035, section 2.3.4 - https://www.ietf.org/rfc/rfc1035.txt
domain_label_validator = RegexValidator(
    regex=r"^(?!-)[a-z]{1,63}(?<!-)$",
    message="Domain have to be 1-63 characters long, contain only alphanumeric characters or hyphens, and must not start or end with a hyphen.",
)


class SubTenantModel(models.Model):
    class Meta:
        abstract = True


class Tenant(models.Model):
    tenant_id = models.AutoField(primary_key=True)
    domain = models.CharField(
        max_length=63, unique=True, validators=[domain_label_validator]
    )
    users = models.ManyToManyField(AppUser, through="Tenant2User")

    class Meta:
        db_table = 'public"."database_tenants_tenant'

    def create_tenant_schema(self):
        all_models = apps.get_models()
        with connection.schema_editor() as schema_editor:
            print(f"Creating schema {self.domain}")
            schema_editor.execute(
                f"CREATE SCHEMA {self.domain}; SET search_path TO {self.domain};"
            )
            for model in all_models:
                from database.organizations.models import Organization

                if issubclass(model, Organization):
                    schema_editor.create_model(model)
                elif issubclass(model, SubTenantModel):
                    schema_editor.create_model(model)

        with connection.schema_editor() as schema_editor:
            schema_editor.execute("SET search_path TO public;")  # Reset schema

    def save(self, *args, **kwargs):
        self.create_tenant_schema()
        super().save(*args, **kwargs)

    def drop_tenant_schema(self):
        with connection.cursor() as cursor:
            cursor.execute(f"DROP SCHEMA {self.domain};")

    def delete(self, *args, **kwargs):
        self.drop_tenant_schema()
        super().delete(*args, **kwargs)


class Tenant2User(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'public"."database_tenants_tenant2user'
