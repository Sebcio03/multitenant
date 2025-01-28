from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.departments.serializers import DepartmentSerializer
from database.departments.models import Department


class DepartmentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        organization = self.request.query_params.get("organization", None)
        if organization is None or not organization.isdigit():
            return Department.objects.none()
        return Department.objects.filter(organization_id=int(organization))
