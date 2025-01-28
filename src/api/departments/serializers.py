from rest_framework import serializers

from database.departments.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "organization"]
        read_only_fields = ["id"]
