from rest_framework import serializers

from database.organizations.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "tenant_id"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        organization = Organization.objects.create(
            tenant_id=int(self.context["request"].COOKIES["tenant_id"])
        )
        return organization
