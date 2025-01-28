from rest_framework import serializers

from database.tenants.models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["tenant_id", "domain"]
        read_only_fields = ["tenant_id"]

    def create(self, validated_data):
        tenant = Tenant.objects.create(domain=validated_data["domain"])
        tenant.users.add(self.context["request"].user)
        return tenant
